"""Thin shell — reclaim per-PR MotherDuck databases and Dives (AC-29).

Invoked by `database-cleanup.yml` on two triggers:
  - `pull_request_target: closed`  — CLEANUP_PR_NUMBER set to the closed PR
  - `schedule` / `workflow_dispatch` — CLEANUP_PR_NUMBER unset; sweep orphans

Owns every I/O seam (MotherDuck connection, `gh api` for open-PR list,
DROP DATABASE / MD_DROP_DIVE execution). Filtering and drop-set derivation
live in the pure `ci_database` thin interfaces.
"""
import json
import os
import subprocess
import sys

import duckdb

import ci_database
import runner_io


def _fetch_open_pr_numbers(repo: str) -> list[int]:
    """Return open PR numbers for `repo` via `gh api`."""
    result = subprocess.run(
        ["gh", "api", "--paginate", f"repos/{repo}/pulls?state=open&per_page=100"],
        capture_output=True, text=True, check=True,
    )
    return [int(pr["number"]) for pr in json.loads(result.stdout)]


def main() -> None:
    token = os.environ["MOTHERDUCK_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    closed_pr_env = os.environ.get("CLEANUP_PR_NUMBER")
    closed_pr_number = int(closed_pr_env) if closed_pr_env else None

    runner_io.mask(token)

    con = duckdb.connect(f"md:?motherduck_token={token}")
    rows = con.execute("SHOW DATABASES;").fetchall()
    all_db_names = [r[0] for r in rows]
    pr_dbs = ci_database.filter_pr_databases(all_db_names)

    if closed_pr_number is not None:
        open_pr_numbers: list[int] = []
        trigger = f"pr-close (PR #{closed_pr_number})"
    else:
        open_pr_numbers = _fetch_open_pr_numbers(repo)
        trigger = "scheduled sweep"

    drop_list = ci_database.databases_to_drop(
        pr_databases=pr_dbs,
        open_pr_numbers=open_pr_numbers,
        closed_pr_number=closed_pr_number,
    )

    print(
        f"cleanup_runner: trigger={trigger} pr_databases={len(pr_dbs)} "
        f"to_drop={len(drop_list)}",
        flush=True,
    )

    failures: list[tuple[str, str]] = []
    for name in drop_list:
        sql = ci_database.drop_database_sql(name)
        print(f"  -> {sql}", flush=True)
        try:
            con.execute(sql)
        except Exception as exc:  # best-effort: log and continue
            print(f"     FAILED: {exc}", file=sys.stderr, flush=True)
            failures.append((name, str(exc)))

    # AC-29: drop per-PR Dives alongside databases (list-and-match by title)
    dive_rows = con.execute(ci_database.list_dives_sql()).fetchall()
    all_dives = [{"id": r[0], "title": r[1]} for r in dive_rows]
    pr_dives = ci_database.filter_pr_dives(all_dives)
    dive_ids_to_drop = ci_database.dives_to_drop(
        pr_dives=pr_dives,
        open_pr_numbers=open_pr_numbers,  # [] on PR-close path; unused when closed_pr_number set
        closed_pr_number=closed_pr_number,
    )

    print(
        f"cleanup_runner: pr_dives={len(pr_dives)} dives_to_drop={len(dive_ids_to_drop)}",
        flush=True,
    )

    for dive_id in dive_ids_to_drop:
        sql = ci_database.drop_dive_sql(dive_id)
        print(f"  -> {sql}", flush=True)
        try:
            con.execute(sql)
        except Exception as exc:  # best-effort: log and continue; appends to shared failures list
            print(f"     FAILED: {exc}", file=sys.stderr, flush=True)
            failures.append((dive_id, str(exc)))

    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
