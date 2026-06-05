# VD-2295 Gate 2 Validation

CI validation stub for testing the stale-SHA MotherDuck database cleanup feature.

## Models modified

- `stg_salescloud__opportunity` — trivial comment bump to trigger Gate 2 for VD-2295 validation
- `fct_opportunity_closed_won` — downstream descendant of stg_salescloud__opportunity
- `fct_pipeline` — downstream descendant of stg_salescloud__opportunity
- `fct_pipeline_monthly_product` — downstream descendant of stg_salescloud__opportunity
- `fct_sales_pipeline_by_stage` — downstream descendant of stg_salescloud__opportunity
