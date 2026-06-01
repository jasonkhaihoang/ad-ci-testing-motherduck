"""Thin shell for ci/design-drift (MotherDuck).

gather → call → dispatch:
  1. Read design.md, manifest.json, modified.json from disk.
  2. Fetch CLAUDE_API_KEY from Azure Key Vault.
  3. Build prompt; POST to Claude API; receive structured JSON via tool-use.
  4. Call run_design_drift (pure).
  5. Post ci/design-drift status; sys.exit(1) on drift or error.

All gate logic lives in design_drift.run_design_drift; this module owns only I/O.

Usage:
    design_drift_runner.py \\
        --pr-number 42 --head-sha abc123 --intent-id intent/sales \\
        --manifest target/manifest.json \\
        --modified reports/modified.json \\
        --claude-api-key-kv-name claude-api-key

Environment:
    GITHUB_REPOSITORY, GH_TOKEN, GITHUB_RUN_ID, GITHUB_SERVER_URL  (status post)
    AZURE_KEYVAULT_URL                                              (consumed by kv_utils)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

import emit_status
import kv_utils
import notify_render
import pr_comment

from design_drift import build_llm_prompt, run_design_drift

CONTEXT = "ci/design-drift"
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = "claude-sonnet-4-6"
CLAUDE_API_VERSION = "2023-06-01"
MAX_OUTPUT_TOKENS = 4096

_DRIFT_TOOL = {
    "name": "report_design_drift",
    "description": "Return drift findings comparing design.md against the modified dbt models.",
    "input_schema": {
        "type": "object",
        "required": ["has_drift", "findings"],
        "properties": {
            "has_drift": {"type": "boolean"},
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["kind", "model", "detail"],
                    "properties": {
                        "kind": {
                            "type": "string",
                            "enum": [
                                "missing_model", "extra_model",
                                "grain_mismatch", "materialization_mismatch",
                                "unique_key_mismatch",
                                "unexpected_column", "missing_column",
                            ],
                        },
                        "model": {"type": "string"},
                        "detail": {"type": "string"},
                    },
                },
            },
        },
    },
}


def _read_text(path: str) -> str:
    with open(path) as f:
        return f.read()


def _design_md_path(intent_id: str) -> str:
    return f"{intent_id}/design.md"


def call_claude(api_key: str, prompt: str) -> dict:
    body = json.dumps({
        "model": CLAUDE_MODEL,
        "max_tokens": MAX_OUTPUT_TOKENS,
        "temperature": 0,
        "tools": [_DRIFT_TOOL],
        "tool_choice": {"type": "tool", "name": "report_design_drift"},
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(CLAUDE_API_URL, data=body, method="POST")
    req.add_header("x-api-key", api_key)
    req.add_header("anthropic-version", CLAUDE_API_VERSION)
    req.add_header("content-type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Claude API HTTP {e.code}: {e.read().decode(errors='replace')}") from e
    for block in payload.get("content", []):
        if block.get("type") == "tool_use" and block.get("name") == "report_design_drift":
            return block.get("input", {})
    raise RuntimeError("Claude response did not include a report_design_drift tool_use block")


def _run_url() -> str:
    base = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    return f"{base}/{repo}/actions/runs/{run_id}"


def _post(head_sha: str, state: str, description: str) -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    emit_status.emit_status(repo, head_sha, CONTEXT, state, description, _run_url())


def _post_pr_comment(pr_number: str, result: dict | None, modified_names: list[str] | None = None) -> None:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not repo:
        return
    body = notify_render.render_design_drift_comment(result, modified_names)
    try:
        pr_comment.upsert(notify_render.DESIGN_DRIFT_MARKER, body, pr_number, repo)
    except Exception as e:
        print(f"Failed to post PR comment: {e}", flush=True)


def _summary(result: dict) -> str:
    if not result["has_drift"]:
        return "design.md matches state:modified — no drift"
    kinds = sorted({f["kind"] for f in result["findings"]})
    return f"design drift detected: {', '.join(kinds)}"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr-number", required=True)
    parser.add_argument("--head-sha", required=True)
    parser.add_argument("--intent-id", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--modified", required=True)
    parser.add_argument("--claude-api-key-kv-name", required=True)
    args = parser.parse_args(argv)

    try:
        design_text = _read_text(_design_md_path(args.intent_id))
        manifest = json.loads(_read_text(args.manifest))
        modified_names = json.loads(_read_text(args.modified))
        api_key = kv_utils.get_secret(args.claude_api_key_kv_name)
        prompt = build_llm_prompt(design_text, manifest, modified_names)
        llm_response = call_claude(api_key, prompt)
    except Exception as e:  # gather/call failure → emit failure status, exit 1
        _post(args.head_sha, "failure", f"design-drift error: {type(e).__name__}: {e}")
        _post_pr_comment(args.pr_number, result=None)
        return 1

    result = run_design_drift(design_text, manifest, modified_names, llm_response)
    _post(args.head_sha, "failure" if result["has_drift"] else "success", _summary(result))
    _post_pr_comment(args.pr_number, result=result, modified_names=modified_names)
    return 1 if result["has_drift"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
