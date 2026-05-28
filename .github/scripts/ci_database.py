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


def drop_database_sql(name: str) -> str:
    """Render DROP DATABASE <name>."""
    return f"DROP DATABASE {name};"


def filter_pr_databases(all_db_names: Iterable[str]) -> list[str]:
    """Return only well-formed per-PR database names (`pr_<digits>_<hex>`)."""
    return [n for n in all_db_names if _PR_DB_RE.match(n)]


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
