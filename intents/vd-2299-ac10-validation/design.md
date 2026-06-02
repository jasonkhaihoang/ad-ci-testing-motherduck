# Intent: vd-2299-ac10-validation

## Summary

Bump the account staging model and add a new dim_industry mart to validate AC-10 (MotherDuck Dive + local dbt snippet in the ci/run comment) end-to-end.

## Models modified

### `stg_salescloud__account` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce account (excluding soft-deleted records)
- **Change:** comment-only validation bump — no structural change to columns, grain, or materialization

## Models added

### `dim_industry` (new)

- **Materialization:** table
- **Grain:** one row per distinct industry value
- **Columns:** industry (PK), account_count
- **Upstream refs:** stg_salescloud__account
- **Purpose:** Industry dimension for market segmentation analysis; validates that the ci/run comment shows a MotherDuck Dive link and local dbt snippet for the new model
