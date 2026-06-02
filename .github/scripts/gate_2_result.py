"""Gate 2 result assembly — pure function, no I/O.

Converts raw inputs (DB creation outcome, dbt run_results.json content,
head SHA, optional error string) into the result dict consumed by
notify_render.render_gate_2_comment().
"""
from __future__ import annotations


def _map_model(result: dict, manifest_materializations: dict[str, str] | None = None) -> dict:
    node = result.get("node") or {}
    name = node.get("name") or result.get("unique_id", "").split(".")[-1]
    rows_affected = (result.get("adapter_response") or {}).get("rows_affected")
    materialization = (node.get("config") or {}).get("materialized", "")
    if not materialization:
        materialization = (manifest_materializations or {}).get(name, "")
    return {
        "name": name,
        "status": result.get("status", ""),
        "rows": rows_affected if rows_affected is not None else None,
        "materialization": materialization,
    }


def assemble(
    db_created: bool,
    run_results: dict | None,
    head_sha: str,
    error: str | None = None,
    manifest_materializations: dict[str, str] | None = None,
) -> dict:
    """Return the gate-2 result dict for render_gate_2_comment().

    Args:
        db_created: True if CREATE DATABASE pr_<N>_<sha> FROM prd succeeded.
        run_results: Parsed dbt run_results.json content, or None if dbt did not run.
        head_sha: PR head SHA (short or full; passed through to the renderer).
        error: Non-None string for transport/auth failures (renders as session_error).
    """
    if error is not None:
        return {
            "overall_status": "error",
            "session_error": error,
            "head_sha": head_sha,
            "clone": {"status": "fail", "models": []},
            "build": {"status": "fail", "models": []},
        }

    clone_status = "pass" if db_created else "fail"

    raw_results = (run_results or {}).get("results") or []
    build_models = [_map_model(r, manifest_materializations or {}) for r in raw_results]
    build_failed = any(
        m["status"] not in ("success", "pass") for m in build_models
    )
    build_status = "fail" if build_failed else "pass"

    overall = "pass" if (db_created and not build_failed) else "fail"

    return {
        "overall_status": overall,
        "head_sha": head_sha,
        "clone": {"status": clone_status, "models": []},
        "build": {"status": build_status, "models": build_models},
    }
