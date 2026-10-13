---
artifacts: [stg_salescloud__opportunity, no_such_model]
---
# stg_salescloud__opportunity

## Grain

One row per Salesforce opportunity.

## Decisions

- **D-01** Materialized as a view over `source('salescloud', 'opportunity')`.
