# Gate-3/Gate-4 dbt deps Fix Validation (VD-2289/VD-2290)

## Changes

Four changes in this PR:

1. `stg_salescloud__account`: existing view. Comment bump for CI validation.
2. `stg_salescloud__opportunity`: existing view. Comment bump from prior commit.
3. `dim_opportunity_stage`: new table. Aggregates opportunity pipeline volume by sales stage.
4. `dim_opportunity_summary`: new table. Aggregates opportunity counts and amounts by sales stage.

## Models

### stg_salescloud__account

Materialization: view
Grain: one row per account (account_id)
Change: comment-only validation marker added. No structural changes.
Columns: account_id, account_name, account_type, billing_city, billing_country, billing_state, created_date, industry, is_deleted, last_modified_date, owner_id.

### stg_salescloud__opportunity

Materialization: view
Grain: one row per opportunity (opportunity_id)
Change: comment-only validation marker updated. No structural changes.
Columns: account_id, amount, close_date, created_date, expected_revenue, fiscal_quarter, fiscal_year, is_closed, is_deleted, is_won, last_modified_date, last_stage_change_date, lead_source, opportunity_id, opportunity_name, opportunity_type, owner_id, probability, stage_name, system_modified_timestamp.

### dim_opportunity_stage

Materialization: table
Grain: one row per stage_name
Change: new model.
Columns: avg_probability, lost_count, open_count, opportunity_count, stage_name, total_amount, won_count.

### dim_opportunity_summary

Materialization: table
Grain: one row per stage_name
Change: new model.
Columns: avg_amount, lost_count, opportunity_count, stage_name, total_amount, won_count.

### dim_account

Materialization: table
Grain: one row per account (account_id)
Change: none — downstream of stg_salescloud__account, no direct modifications.
Columns: account_id, account_name, account_type, billing_city, billing_country, billing_state, created_date, industry, last_modified_date, owner_id.

### fct_pipeline

Materialization: table
Grain: one row per opportunity (opportunity_id)
Change: none — downstream of stg_salescloud__account and stg_salescloud__opportunity, no direct modifications.
Columns: account_id, account_name, account_type, amount, billing_city, billing_country, billing_state, close_date, created_date, days_in_current_stage, expected_revenue, forecast_category, industry, is_closed, is_orphaned_opportunity, is_won, is_zero_value, last_modified_date, last_stage_change_date, lead_source, opportunity_age_days, opportunity_id, opportunity_name, opportunity_type, owner_email, owner_id, owner_is_active, owner_name, probability, sales_cycle_days, stage_name, system_modified_timestamp, weighted_amount.

### fct_pipeline_monthly_product

Materialization: table
Grain: one row per (close_month, product_id)
Change: none — downstream, no direct modifications.
Columns: avg_deal_size, avg_discount, avg_unit_price, close_month, earliest_close_date, latest_close_date, line_item_count, lost_opportunity_count, lost_revenue, opportunity_count, product_code, product_id, product_name, total_quantity, total_revenue, win_rate_pct, won_opportunity_count, won_revenue.

### fct_sales_pipeline_by_stage

Materialization: table
Grain: one row per (stage_name, fiscal_year, fiscal_quarter)
Change: none — downstream, no direct modifications.
Columns: avg_probability, fiscal_quarter, fiscal_year, lost_count, opportunity_count, stage_name, total_amount, weighted_amount, won_count.
