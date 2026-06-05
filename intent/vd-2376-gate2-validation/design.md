# Design: VD-2376 Gate-2 Validation

Validation intent for VD-2376 — MotherDuck Dive cleanup alongside database on PR close.

## Models modified

### `stg_salescloud__opportunity` (modified)

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity (excluding soft-deleted records)
- **Change:** comment-only validation bump — no structural change to columns, grain, or materialization
- **Columns:** opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, created_date, close_date, last_stage_change_date, is_closed, is_won, is_deleted, last_modified_date, system_modified_timestamp, fiscal_quarter, fiscal_year

### `dim_opportunity_stage` (new)

- **Materialization:** table
- **Grain:** one row per distinct opportunity stage_name
- **Columns:** stage_name, opportunity_count, open_count, won_count, lost_count, total_amount, open_amount, won_amount, avg_probability
- **Upstream refs:** stg_salescloud__opportunity

## Downstream models (no structural change — included in state:modified+ closure)

### `stg_salescloud__account`

- **Materialization:** view
- **Grain:** one row per Salesforce account
- **Columns:** account_id, account_type, industry, billing_city, billing_state, billing_country, owner_id, is_deleted, created_date, last_modified_date

### `stg_salescloud__user`

- **Materialization:** view
- **Grain:** one row per Salesforce user
- **Columns:** user_id, user_name, email, username, user_role_id, profile_id, job_title, is_active, created_date, last_modified_date

### `stg_salescloud__opportunitylineitem`

- **Materialization:** view
- **Grain:** one row per Salesforce opportunity line item
- **Columns:** line_item_id, opportunity_id, pricebook_entry_id, product_id, product_name, product_code, quantity, unit_price, total_price, discount, description, service_date, sort_order, created_date

### `dim_account`

- **Materialization:** table
- **Grain:** one row per Salesforce account
- **Columns:** account_id, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_id, created_date, last_modified_date

### `dim_user`

- **Materialization:** table
- **Grain:** one row per Salesforce user
- **Columns:** user_id, user_name, email, username, job_title, user_role_id, profile_id, is_active, created_date, last_modified_date

### `fct_opportunity_closed_won`

- **Materialization:** table
- **Grain:** one row per closed-won opportunity
- **Columns:** opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, fiscal_quarter, fiscal_year, sales_cycle_days, account_name, account_type, industry, billing_country, owner_name, owner_email

### `fct_pipeline`

- **Materialization:** table
- **Grain:** one row per opportunity
- **Columns:** opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, last_stage_change_date, is_closed, is_won, forecast_category, sales_cycle_days, opportunity_age_days, days_in_current_stage, is_orphaned_opportunity, is_zero_value, last_modified_date, system_modified_timestamp, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_name, owner_email, owner_is_active

### `fct_pipeline_monthly_product`

- **Materialization:** table
- **Grain:** one row per product per close_month
- **Columns:** close_month, product_id, product_code, product_name, total_revenue, won_revenue, lost_revenue, opportunity_count, won_opportunity_count, lost_opportunity_count, total_quantity, line_item_count, avg_deal_size, avg_unit_price, avg_discount, earliest_close_date, latest_close_date

### `fct_sales_pipeline_by_stage`

- **Materialization:** table
- **Grain:** one row per stage per fiscal quarter per fiscal year
- **Columns:** stage_name, fiscal_year, fiscal_quarter, opportunity_count, won_count, lost_count, total_amount, weighted_amount, avg_probability
