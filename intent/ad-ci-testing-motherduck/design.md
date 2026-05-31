# Sales Pipeline CI Testing — Design

## Summary of Changes

Two changes in this PR:
1. `stg_salescloud__opportunity` — new derived column `fiscal_half` (H1 for Jan–Jun, H2 for Jul–Dec)
2. `fct_pipeline_won_by_rep` — new table aggregating won opportunities by rep and fiscal period

## Models

### stg_salescloud__opportunity

Materialization: view  
Grain: one row per Salesforce opportunity (source: salescloud.opportunity, filtered isdeleted=false)  
Change: fiscal_half column added

Columns: opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, created_date, close_date, last_stage_change_date, is_closed, is_won, is_deleted, last_modified_date, system_modified_timestamp, fiscal_quarter, fiscal_year, fiscal_half

### fct_pipeline

Materialization: table  
Grain: one row per opportunity (current state snapshot)  
Change: none — downstream rebuild only

Columns: opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, last_stage_change_date, is_closed, is_won, forecast_category, sales_cycle_days, opportunity_age_days, days_in_current_stage, is_orphaned_opportunity, is_zero_value, last_modified_date, system_modified_timestamp, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_name, owner_email, owner_is_active

### fct_pipeline_monthly_product

Materialization: table  
Grain: one row per (close_month, product_id)  
Change: none — downstream rebuild only

Columns: close_month, product_id, product_code, product_name, total_revenue, won_revenue, lost_revenue, opportunity_count, won_opportunity_count, lost_opportunity_count, total_quantity, line_item_count, avg_deal_size, avg_unit_price, avg_discount, win_rate_pct, earliest_close_date, latest_close_date

### fct_sales_pipeline_by_stage

Materialization: table  
Grain: one row per (stage_name, fiscal_year, fiscal_quarter)  
Change: none — downstream rebuild only

Columns: stage_name, fiscal_year, fiscal_quarter, opportunity_count, won_count, lost_count, total_amount, weighted_amount, avg_probability

### fct_pipeline_won_by_rep

Materialization: table  
Grain: one row per (owner_id, fiscal_year, fiscal_quarter)  
Change: new model in this PR

Reads from fct_pipeline filtered to is_won=true. Groups by rep and fiscal period.

Columns: rep_period_id, owner_id, owner_name, owner_email, owner_is_active, fiscal_quarter, fiscal_year, won_opportunities_count, total_won_amount, total_weighted_amount, avg_sales_cycle_days, min_sales_cycle_days, max_sales_cycle_days, first_close_date, last_close_date
