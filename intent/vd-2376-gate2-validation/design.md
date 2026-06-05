# Design: VD-2376 Gate-2 Validation

Validation intent for VD-2376 — MotherDuck Dive cleanup alongside database on PR close.

## Models modified

### `stg_salescloud__opportunity` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity (excluding soft-deleted records)
- **Change:** comment-only validation bump — no structural change to columns, grain, or materialization
- **Columns:** opportunity_id (PK), account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, created_date, close_date, last_stage_change_date, is_closed, is_won, is_deleted, last_modified_date, system_modified_timestamp, fiscal_quarter, fiscal_year

### `dim_opportunity_stage` (new)

- **Materialization:** table
- **Grain:** one row per distinct opportunity stage_name
- **Columns:** stage_name (PK), opportunity_count, open_count, won_count, lost_count, total_amount, open_amount, won_amount, avg_probability
- **Upstream refs:** stg_salescloud__opportunity
- **Purpose:** Stage-level pipeline summary for reporting on opportunity distribution by stage

## Downstream models (no structural change — included in state:modified+ closure)

### `stg_salescloud__account`

- **Materialization:** view
- **Grain:** one row per Salesforce account

### `stg_salescloud__user`

- **Materialization:** view
- **Grain:** one row per Salesforce user

### `stg_salescloud__opportunitylineitem`

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity line item

### `dim_account`

- **Materialization:** table
- **Grain:** one row per Salesforce account

### `dim_user`

- **Materialization:** table
- **Grain:** one row per Salesforce user

### `fct_opportunity_closed_won`

- **Materialization:** table
- **Grain:** one row per closed-won opportunity

### `fct_pipeline`

- **Materialization:** table
- **Grain:** one row per opportunity

### `fct_pipeline_monthly_product`

- **Materialization:** table
- **Grain:** one row per product per close_month

### `fct_sales_pipeline_by_stage`

- **Materialization:** table
- **Grain:** one row per stage per fiscal quarter per fiscal year
