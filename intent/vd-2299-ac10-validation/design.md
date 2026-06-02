# Intent: vd-2299-ac10-validation

## Summary

Bump the account staging model and add a new dim_industry mart to validate AC-10 (MotherDuck Dive + local dbt snippet in the ci/run comment) end-to-end.

## Models modified

### `stg_salescloud__account` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce account (excluding soft-deleted records)
- **Change:** comment-only validation bump — no structural change to columns, grain, or materialization

### `dim_account` (modified — descendant)

- **Materialization:** table
- **Grain:** one row per account (account_id is the natural unique key)
- **Columns:** account_id, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_id, created_date, last_modified_date
- **Change:** no structural change — pulled into closure as downstream of `stg_salescloud__account`

### `fct_pipeline` (modified — descendant)

- **Materialization:** table
- **Grain:** one row per open pipeline opportunity
- **Change:** no structural change — pulled into closure as downstream of `stg_salescloud__account`

## Models added

### `dim_industry` (new)

- **Materialization:** table
- **Grain:** one row per distinct industry value
- **Columns:** industry (unique, not_null — enforced by dbt tests; no unique_key config, table materialization), account_count
- **Upstream refs:** stg_salescloud__account
- **Purpose:** Industry dimension for market segmentation analysis; validates that the ci/run comment shows a MotherDuck Dive link and local dbt snippet for the new model
