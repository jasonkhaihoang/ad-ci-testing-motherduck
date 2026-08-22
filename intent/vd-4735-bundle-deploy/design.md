# CI verification design stub — VD-4735 (MotherDuck dbt Quality bundle deploy)

This branch deploys CI infrastructure only (workflow YAML, an isolated dbt-quality
profile, shared script updates, and a `packages.yml` addition) to validate
`domain-ci-motherduck-bundle`'s new `dbt-project-quality.yml` workflow end-to-end.
No dbt model is added, removed, or restructured by this branch.

Gate 1 on this fixture repo currently has no prior successful prod-manifest
publish, so `state:modified` resolves in **greenfield mode** — the full
project graph, not just this branch's own diff. The design below therefore
describes the whole Sales Pipeline mart as it exists today, so this gate
compares against the real project shape rather than an empty baseline.

## Models

### Staging layer (views)

- **`stg_salescloud__opportunity`** — one row per Salesforce opportunity (excluding soft-deleted records).
- **`stg_salescloud__account`** — one row per Salesforce account.
- **`stg_salescloud__user`** — one row per Salesforce user (sales rep / opportunity owner).
- **`stg_salescloud__opportunitylineitem`** — one row per opportunity line item.

### Dimension layer (tables)

- **`dim_account`** — one row per account, keyed on `account_id`.
- **`dim_user`** — one row per user, keyed on `user_id`.

### Mart layer (tables)

- **`fct_pipeline`** — one row per open/in-flight opportunity, keyed on `opportunity_id`; joins `stg_salescloud__opportunity` with `dim_account` and `dim_user`.
- **`fct_opportunity_closed_won`** — one row per closed-won opportunity, keyed on `opportunity_id`.
- **`fct_pipeline_monthly_product`** — monthly, product-level aggregate of pipeline/closed-won activity, grained on close month + product.
- **`fct_sales_pipeline_by_stage`** — pipeline aggregated by sales stage, grained on stage (and typically rep/period).

No column-level contract is asserted here beyond each model's primary key
noted above — see each model's `schema.yml` for the authoritative column
list and descriptions.
