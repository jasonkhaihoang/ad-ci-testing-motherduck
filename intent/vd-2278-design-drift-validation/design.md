# Design — VD-2278 design-drift validation

## stg_salescloud__opportunity
- grain: one row per opportunity (opportunity_id)
- materialization: view
- columns: opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, created_date, close_date, last_stage_change_date, is_closed, is_won, is_deleted, last_modified_date, system_modified_timestamp, fiscal_quarter, fiscal_year

## fct_pipeline
- grain: one row per opportunity (opportunity_id)
- materialization: table
- columns: opportunity_id, account_id, owner_id, opportunity_name, stage_name, opportunity_type, lead_source, amount, probability, expected_revenue, weighted_amount, created_date, close_date, last_stage_change_date, is_closed, is_won, forecast_category, sales_cycle_days, opportunity_age_days, days_in_current_stage, is_orphaned_opportunity, is_zero_value, last_modified_date, system_modified_timestamp, account_name, account_type, industry, billing_city, billing_state, billing_country, owner_name, owner_email, owner_is_active

## fct_pipeline_monthly_product
- grain: one row per close_month + product_id
- materialization: table
- columns: close_month, product_id, product_code, product_name, total_revenue, won_revenue, lost_revenue, opportunity_count, won_opportunity_count, lost_opportunity_count, total_quantity, line_item_count, avg_deal_size, avg_unit_price, avg_discount, win_rate_pct, earliest_close_date, latest_close_date

## fct_sales_pipeline_by_stage
- grain: one row per stage_name + fiscal_year + fiscal_quarter
- materialization: table
- columns: stage_name, fiscal_year, fiscal_quarter, opportunity_count, won_count, lost_count, total_amount, weighted_amount, avg_probability

## fct_won_opportunities
- grain: one row per closed-won opportunity (opportunity_id)
- materialization: table
- unique_key: opportunity_id
- columns: opportunity_id, account_id, owner_id, close_date, fiscal_quarter, fiscal_year, arr, stage_name
