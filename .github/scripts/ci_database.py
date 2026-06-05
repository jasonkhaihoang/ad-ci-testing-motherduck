"""Per-PR MotherDuck database lifecycle — pure SQL emission + drop-set derivation.

All functions are pure: no I/O, no live DB connections. SQL strings are
returned for the caller to execute via dbt-duckdb or a direct md: connection.
"""
import re
from typing import Iterable

_PR_DB_RE = re.compile(r"^pr_(\d+)_[0-9a-f]+$")


def derive_ci_database_name(pr_number: int, head_sha_short: str) -> str:
    """Deterministic per-PR database name: pr_{pr_number}_{head_sha_short}."""
    return f"pr_{pr_number}_{head_sha_short}"


def create_database_from_prod_sql(name: str, prod_db_name: str = "prd") -> str:
    """Render CREATE DATABASE <name> FROM <prod_db_name>."""
    return f"CREATE DATABASE {name} FROM {prod_db_name};"


def clear_db_retention_sql(db_name: str) -> str:
    """Render ALTER DATABASE <db_name> SET SNAPSHOT_RETENTION_DAYS = 0.

    Called as a fallback when CREATE DATABASE … FROM <db_name> fails because
    <db_name> has >0 snapshot retention incompatible with a free-plan account.
    After this call the clone can be retried. No-op on databases that already
    have 0-day retention.
    """
    return f"ALTER DATABASE {db_name} SET SNAPSHOT_RETENTION_DAYS = 0;"


def drop_database_sql(name: str) -> str:
    """Render DROP DATABASE <name>."""
    return f"DROP DATABASE {name};"


def filter_pr_databases(all_db_names: Iterable[str]) -> list[str]:
    """Return only well-formed per-PR database names (`pr_<digits>_<hex>`)."""
    return [n for n in all_db_names if _PR_DB_RE.match(n)]


def stale_pr_databases(
    pr_databases: Iterable[str],
    pr_number: int,
    current_db_name: str,
) -> list[str]:
    """Return databases for `pr_number` that are not `current_db_name`.

    Used by the gate-2 push-cleanup step to drop stale per-SHA databases
    immediately after the new one is confirmed created.
    """
    result: list[str] = []
    for name in pr_databases:
        m = _PR_DB_RE.match(name)
        if not m:
            continue
        if int(m.group(1)) == pr_number and name != current_db_name:
            result.append(name)
    return result


def databases_to_drop(
    pr_databases: Iterable[str],
    open_pr_numbers: Iterable,
    closed_pr_number: int | None,
) -> list[str]:
    """Derive the set of per-PR databases to drop.

    - When `closed_pr_number` is given (PR-close trigger), return every database
      belonging to that PR — including multiple SHAs from prior force-pushes.
    - When `closed_pr_number` is None (scheduled sweep), return every database
      whose PR number is not in `open_pr_numbers` (orphans).
    """
    open_set = {int(n) for n in open_pr_numbers}
    result: list[str] = []
    for name in pr_databases:
        m = _PR_DB_RE.match(name)
        if not m:
            continue
        pr_num = int(m.group(1))
        if closed_pr_number is not None:
            if pr_num == int(closed_pr_number):
                result.append(name)
        else:
            if pr_num not in open_set:
                result.append(name)
    return result


def _schema_from_relation_name(relation_name: str) -> str:
    """Extract schema from a dbt relation_name like '"db"."stg"."model"'."""
    if not relation_name:
        return ""
    parts = relation_name.replace('"', '').split('.')
    return parts[1] if len(parts) == 3 else ""


def extract_model_schemas(run_results: dict | None) -> dict[str, str]:
    """Extract {model_name: schema} from dbt run_results.json.

    Reads the top-level relation_name field (e.g. '"db"."stg"."model"') to get
    the actual rendered schema. Falls back to node.schema, then to 'main'.
    node.schema holds the profile-level default, not the custom schema override.
    """
    result: dict[str, str] = {}
    for r in (run_results or {}).get("results", []):
        node = r.get("node") or {}
        name = node.get("name") or r.get("unique_id", "").split(".")[-1]
        schema = (
            _schema_from_relation_name(r.get("relation_name") or "")
            or node.get("schema")
            or "main"
        )
        if name:
            result[name] = schema
    return result


def build_dive_jsx(db_name: str, model_schemas: dict[str, str]) -> str:
    """Build Dive JSX content with fully-qualified table references.

    Generates useSQLQuery hooks as db_name.schema.model so the Dive resolves
    correctly in any MotherDuck user session, not just the CI runner's.
    Returns an empty string when model_schemas is empty (caller guards on this).
    """
    if not model_schemas:
        return ""
    hooks = "\n  ".join(
        f'const {{ data: {name} }} = useSQLQuery('
        f'"SELECT * FROM {db_name}.{schema}.{name} LIMIT 20");'
        for name, schema in model_schemas.items()
    )
    panels = "\n      ".join(
        f'<div><h2>{name}</h2><pre>{{JSON.stringify({name}, null, 2)}}</pre></div>'
        for name in model_schemas
    )
    return (
        'import { useSQLQuery } from "@motherduck/react-sql-query";\n'
        "export default function Dive() {\n"
        f"  {hooks}\n"
        "  return (\n"
        "    <div>\n"
        f"      {panels}\n"
        "    </div>\n"
        "  );\n"
        "}"
    )


_E2E_SCENARIOS = ("greenfield", "incremental-modify", "incremental-staging")


def build_scenario_matrix(scenario: str) -> list[str]:
    """Expand a `/test-ci-duckdb` scenario input into the list of scenarios to run.

    "all" → every scenario; a single scenario → single-element list.
    Unknown scenario → ValueError.
    """
    if scenario == "all":
        return list(_E2E_SCENARIOS)
    if scenario in _E2E_SCENARIOS:
        return [scenario]
    raise ValueError(
        f"unknown scenario {scenario!r}; expected 'all' or one of {list(_E2E_SCENARIOS)}"
    )


def derive_e2e_db_name(scenario: str, run_id: str) -> str:
    """Derive identifier-safe E2E database name: pr_e2e_<scenario>_<run_id_short>.

    Hyphens in `scenario` are normalised to underscores so the rendered name is a
    valid DuckDB/MotherDuck identifier. `run_id_short` is the first 8 chars of
    `run_id`, lowercased and hyphen-stripped.
    """
    if scenario not in _E2E_SCENARIOS:
        raise ValueError(
            f"unknown scenario {scenario!r}; expected one of {list(_E2E_SCENARIOS)}"
        )
    scenario_safe = scenario.replace("-", "_")
    run_id_short = run_id.lower().replace("-", "")[:8]
    return f"pr_e2e_{scenario_safe}_{run_id_short}"
