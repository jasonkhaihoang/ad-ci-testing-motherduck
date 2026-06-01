# E2E Greenfield Test

## Changes

No model changes. Empty commit to trigger CI greenfield path.

## Context

Automated E2E validation (VD-2283). No prod-manifest baseline exists.
All successful publish-prod-manifest-duckdb runs deleted.
CI builds the full project graph: all models new relative to empty baseline.

## Models

No structural changes. All project models appear in state:modified+ because
there is no prod baseline to compare against.
