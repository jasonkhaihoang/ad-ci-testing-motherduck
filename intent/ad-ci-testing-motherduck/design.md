# Sales Pipeline CI Testing — Design

## Changes

Two changes in this PR:

1. `stg_salescloud__opportunity`: new derived column `fiscal_half` (H1 for Jan–Jun, H2 for Jul–Dec from close date month). This column is intentionally NOT propagated to `fct_pipeline`, `fct_pipeline_monthly_product`, or `fct_sales_pipeline_by_stage` — those marts do not require period-half analysis. `fct_pipeline_won_by_rep` inherits `fiscal_quarter` from `fct_pipeline` but not `fiscal_half` (by design, aggregation is by quarter).

2. `fct_pipeline_won_by_rep`: new table. Reads from `fct_pipeline` filtering `is_won = true`. Groups closed-won opportunities by sales rep per fiscal quarter and year. Grain enforced by GROUP BY on (owner_id, fiscal_year, fiscal_quarter). The `rep_period_id` column is a md5 hash surrogate, not a configured `unique_key`. No config-level `unique_key` is set (materialized as table, not incremental).

## Models

All five models listed below are in `state:modified+`. The three downstream models have no intentional logic changes — they rebuild because `stg_salescloud__opportunity` changed.

### stg_salescloud__opportunity

Materialization: view  
Change: added `fiscal_half` column only. All other columns unchanged.  
Columns (21): opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, created_date, close_date, last_stage_change_date, is_closed, is_won, is_deleted, last_modified_date, system_modified_timestamp, fiscal_quarter, fiscal_year, fiscal_half

### fct_pipeline

Materialization: table  
Change: none (downstream rebuild). `fiscal_half` from stg is intentionally not selected here.  
Columns (33): opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, last_stage_change_date, is_closed, is_won, forecast_category, sales_cycle_days, opportunity_age_days, days_in_current_stage, is_orphaned_opportunity, is_zero_value, last_modified_date, system_modified_timestamp, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_name, owner_email, owner_is_active

### fct_pipeline_monthly_product

Materialization: table  
Change: none (downstream rebuild). Does not use `fiscal_half`.  
Columns (18): close_month, product_id, product_code, product_name, total_revenue, won_revenue, lost_revenue, opportunity_count, won_opportunity_count, lost_opportunity_count, total_quantity, line_item_count, avg_deal_size, avg_unit_price, avg_discount, win_rate_pct, earliest_close_date, latest_close_date

### fct_sales_pipeline_by_stage

Materialization: table  
Change: none (downstream rebuild). Does not use `fiscal_half`.  
Columns (9): stage_name, fiscal_year, fiscal_quarter, opportunity_count, won_count, lost_count, total_amount, weighted_amount, avg_probability

### fct_pipeline_won_by_rep

Materialization: table  
Change: new model.  
Columns (15): rep_period_id, owner_id, owner_name, owner_email, owner_is_active, fiscal_quarter, fiscal_year, won_opportunities_count, total_won_amount, total_weighted_amount, avg_sales_cycle_days, min_sales_cycle_days, max_sales_cycle_days, first_close_date, last_close_date
