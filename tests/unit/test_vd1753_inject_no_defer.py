"""VD-1753: assert injected dbt commands contain no --defer."""

import importlib.util
import os
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / ".github" / "scripts" / "inject_notebook.py"


@pytest.fixture
def inject_module(monkeypatch):
    monkeypatch.setenv("EPHEMERAL_WORKSPACE_ID", "ws-id")
    monkeypatch.setenv("EPHEMERAL_WORKSPACE_NAME", "ws-name")
    monkeypatch.setenv("EPHEMERAL_LAKEHOUSE_ID", "lh-id")
    monkeypatch.setenv("HEAD_BRANCH", "feature/test")
    monkeypatch.setenv("REPO_URL", "https://github.com/example/repo")
    spec = importlib.util.spec_from_file_location("inject_notebook", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["inject_notebook"] = mod
    spec.loader.exec_module(mod)
    return mod


def _minimal_nb():
    return {
        "cells": [
            {"cell_type": "code", "source": ["# Parameters\n"], "metadata": {"tags": ["parameters"]}, "outputs": [], "execution_count": None},
            {"cell_type": "code", "source": ["run_dbt_job(...)\n"], "metadata": {}, "outputs": [], "execution_count": None},
        ],
        "metadata": {},
    }


def test_parameters_cell_has_no_defer(inject_module):
    nb, idx = inject_module.substitute_parameters_cell(_minimal_nb())
    source = "".join(nb["cells"][idx]["source"])
    assert "--defer" not in source
    assert "dbt build --select state:modified+" in source
    assert "--state {prod_state_path}" in source


def test_clone_cell_has_no_defer(inject_module):
    nb, idx = inject_module.substitute_parameters_cell(_minimal_nb())
    nb = inject_module.insert_clone_cell(nb, idx)
    all_source = "".join("".join(c.get("source", [])) for c in nb["cells"])
    assert "dbt clone" in all_source
    assert "--defer" not in all_source
