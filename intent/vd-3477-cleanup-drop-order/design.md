# VD-3477 cleanup drop-order backport

## Changes

No dbt model changes. This intent updates `.github/scripts/cleanup_runner.py`
only, swapping the MotherDuck cleanup drop order to DROP SHARE before DROP
DATABASE (MotherDuck refuses DROP DATABASE while a share still references it).

## Models

No models modified.
