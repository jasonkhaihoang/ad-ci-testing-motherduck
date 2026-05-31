# Sales Pipeline CI Testing — Design Contract

## Intent

CI validation: add `fiscal_half` to `stg_salescloud__opportunity` and introduce `fct_pipeline_won_by_rep` mart.

## Models in state:modified+

### stg_salescloud__opportunity (modified — view)

**Grain:** One row per Salesforce opportunity (1:1 with source `salescloud.opportunity`)
**Materialization:** `view`
**Unique key:** `opportunity_id`
**Schema:** `stg`

**Changes:** Added `fiscal_half` column (new in this PR).

**All columns:**
- `opportunity_id` (PK, unique, not_null)
- `account_id` (FK)
- `owner_id` (FK)
- `opportunity_name`
- `stage_name`
- `opportunity_type`
- `lead_source`
- `amount`
- `probability`
- `expected_revenue`
- `created_date`
- `close_date`
- `last_stage_change_date`
- `is_closed`
- `is_won`
- `is_deleted`
- `last_modified_date`
- `system_modified_timestamp`
- `fiscal_quarter` (derived: Q1/Q2/Q3/Q4 from close_date month)
- `fiscal_year` (derived: calendar year of close_date)
- `fiscal_half` (derived: H1 for Jan-Jun, H2 for Jul-Dec — new column added in this PR)

---

### fct_pipeline (downstream — table)

**Grain:** One row per opportunity (current snapshot)
**Materialization:** `table`
**Unique key:** `opportunity_id`
**Schema:** `mrt`

No logic changes — downstream dependency of `stg_salescloud__opportunity`, included in state:modified+ automatically.

**All columns:**
- `opportunity_id` (PK, unique, not_null)
- `account_id`
- `owner_id`
- `opportunity_name`
- `stage_name`
- `opportunity_type`
- `lead_source`
- `amount`
- `probability`
- `expected_revenue`
- `weighted_amount`
- `created_date`
- `close_date`
- `last_stage_change_date`
- `is_closed`
- `is_won`
- `forecast_category`
- `sales_cycle_days`
- `opportunity_age_days`
- `days_in_current_stage`
- `is_orphaned_opportunity`
- `is_zero_value`
- `last_modified_date`
- `system_modified_timestamp`
- `account_name`
- `account_type`
- `industry`
- `billing_city`
- `billing_state`
- `billing_country`
- `owner_name`
- `owner_email`
- `owner_is_active`

---

### fct_pipeline_won_by_rep (new — table)

**Grain:** One row per sales rep per fiscal quarter per fiscal year
**Materialization:** `table`
**Unique key:** `rep_period_id` (md5 surrogate key of owner_id + fiscal_year + fiscal_quarter)
**Schema:** `mrt`

Source: filters `fct_pipeline` where `is_won = true`, aggregates by rep and period.

**All columns:**
- `owner_id` (not_null)
- `owner_name`
- `owner_email`
- `owner_is_active`
- `fiscal_quarter` (not_null)
- `fiscal_year` (not_null)
- `rep_period_id` (surrogate PK, unique, not_null)
- `won_opportunities_count`
- `total_won_amount`
- `total_weighted_amount`
- `avg_sales_cycle_days`
- `min_sales_cycle_days`
- `max_sales_cycle_days`
- `first_close_date`
- `last_close_date`
