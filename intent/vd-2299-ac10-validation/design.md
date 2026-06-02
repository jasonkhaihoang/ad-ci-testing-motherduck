# Intent: vd-2299-ac10-validation

## Summary

Bump the account staging model and add a new dim_industry mart to validate AC-10 (MotherDuck Dive + local dbt snippet in the ci/run comment) end-to-end.

## Models modified

### `stg_salescloud__account` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce account
- **Columns:** account_id, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_id, is_deleted, created_date, last_modified_date
- **Change:** comment-only validation bump — no structural change to columns, grain, or materialization

### `dim_account` (modified — descendant)

- **Materialization:** table
- **Grain:** one row per account
- **Change:** no structural change — pulled into closure as downstream of `stg_salescloud__account`

### `fct_pipeline` (modified — descendant)

- **Materialization:** table
- **Grain:** one row per open pipeline opportunity
- **Change:** no structural change — pulled into closure as downstream of `stg_salescloud__account`

## Models added

### `dim_industry` (new)

- **Materialization:** table
- **Grain:** one row per distinct industry value
- **Columns:** industry, account_count
- **Upstream refs:** stg_salescloud__account
- **Purpose:** Industry dimension for market segmentation analysis
