# Design — VD-2278 design-drift validation

## stg_salescloud__opportunity
- grain: one row per opportunity (opportunity_id)
- materialization: view
- unique_key: opportunityid
- columns: opportunityid, accountid, ownerid, closedate, amount, stagename, iswon, fiscal_quarter, fiscal_year

## fct_won_opportunities
- grain: one row per closed-won opportunity (opportunity_id)
- materialization: table
- unique_key: opportunity_id
- columns: opportunity_id, account_id, owner_id, close_date, fiscal_quarter, fiscal_year, arr, stage_name
