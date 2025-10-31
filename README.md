# kpi-library
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![License](https://img.shields.io/badge/license-Apache--2.0-blue)
![Coverage](https://img.shields.io/badge/templates-50%2B-orange)
![SQL](https://img.shields.io/badge/SQL-BigQuery-red)
![Made by](https://img.shields.io/badge/made_by-Chatka-black)


Reusable, BigQuery-ready KPI templates + tiny synthetic seed datasets for agentic analytics systems.
Built by Chatka to accelerate onboarding, demos, and production rollouts across functions (Supply Chain, Finance, Marketing, HR, Product/Engineering).

> Why: Most teams reinvent KPI logic, dimensions, and SQL. This library gives you opinionated, transferable definitions you can map to your warehouse and start reasoning over immediately.




---

What’s inside

Structured KPI templates (YAML) — name, definition, allowed dimensions, example questions, and BigQuery SQL.

Seed CSVs — tiny synthetic tables to demo charts instantly.

Schema & tooling — JSON Schema for validation, seed generators, and helpers.

Domain coverage (v0) — 50 KPIs across Supply Chain, Finance, Marketing, HR, Product/Eng.



---

Repo layout

kpi-library/
  README.md
  schema/
    kpi_schema.json
  kpis/
    supply_chain/*.yaml
    finance/*.yaml
    marketing/*.yaml
    hr/*.yaml
    product_eng/*.yaml
  seeds/
    supply_chain/*.sample.csv
    finance/*.sample.csv
    marketing/*.sample.csv
    hr/*.sample.csv
    product_eng/*.sample.csv
  tools/
    validate.py
    seed_generator.py


---

Example KPI (YAML)

id: delivery_delay
display_name: Delivery Delay (minutes vs promised)
domain: Supply Chain
category: Last Mile
aliases: ["on-time performance", "slot adherence", "lateness"]
description: Average minutes late vs promised delivery slot for fulfilled orders.
grain: day
dimensions:
  - { name: date,   semantic: temporal }
  - { name: region, semantic: geography }
  - { name: cfc,    semantic: facility }
  - { name: spoke,  semantic: facility }
  - { name: carrier, semantic: logistics_partner }
derived_from: [on_time_deliveries]
business_rules:
  late_threshold_min: 5
formula:
  expression: "AVG(TIMESTAMP_DIFF(actual_ts, promised_ts, MINUTE))"
  notes: "Negative values imply early deliveries; cap outliers at P99 if needed."
sql:
  bigquery:
    source_table: your_project.retail_ops.delivery_facts
    metric_view: your_project.analytics_mv.delivery_delay_daily
    params: ["@start_date", "@end_date"]
    query: |
      SELECT
        DATE(delivery_ts) AS date,
        region, cfc, spoke, carrier,
        AVG(TIMESTAMP_DIFF(actual_ts, promised_ts, MINUTE)) AS delivery_delay_min
      FROM `your_project.retail_ops.delivery_facts`
      WHERE delivery_ts BETWEEN @start_date AND @end_date
      GROUP BY 1,2,3,4,5
tests:
  - name: sane_delay_range
    assertion: "delivery_delay_min BETWEEN -120 AND 720"
examples:
  business_questions:
    - "Why did delivery delay rise in South during Q2?"
    - "Which carrier contributed most to delay last week by CFC?"
demo:
  seed_data: seeds/supply_chain/delivery_facts.sample.csv


---

Quickstart

1) Validate templates

pip install pyyaml jsonschema
python tools/validate.py kpis/supply_chain/delivery_delay.yaml

2) Generate/refresh seed data

python tools/seed_generator.py
# writes *.sample.csv into /seeds subfolders

3) Load seeds into BigQuery (example)

bq load --autodetect --replace --source_format=CSV \
  your_project.retail_ops.delivery_facts \
  seeds/supply_chain/delivery_facts.sample.csv

bq load --autodetect --replace --source_format=CSV \
  your_project.finance.facts_pnl \
  seeds/finance/finance_facts.sample.csv

bq load --autodetect --replace --source_format=CSV \
  your_project.marketing.acquisition_facts \
  seeds/marketing/marketing_facts.sample.csv

4) Run the sample SQL from the YAML

Open the YAML, copy the sql.bigquery.query, and set params (@start_date, @end_date).
Optionally create the metric_view referenced in the template.


---

Domains & KPIs (v0)

Supply Chain / Logistics (10)
On-Time Delivery Rate, Delivery Delay, Perfect Order Rate, Supplier Fill Rate, Inventory Accuracy, Days of Inventory, Backorder Rate, Substitution Rate, Route Utilization, Cost per Drop

Finance / Profitability (10)
Revenue, Gross Margin %, Net Margin %, OpEx Ratio, EBITDA, Cash Conversion Cycle, Forecast Accuracy (Rev), Budget Variance %, Unit Economics (per Order), Refund/Return Rate

Marketing / Growth (10)
CAC, ROAS, Conversion Rate, CTR, CPC, CPA, New vs Returning Mix, LTV (cohort), Churn Rate, Email Performance

HR / Workforce / Productivity (10)
Headcount, Attrition Rate, Time to Hire, Offer Acceptance Rate, Absenteeism, Training Hours per FTE, Internal Mobility, Overtime Ratio, Productivity Index, Diversity Mix

Product / Engineering / Ops Tech (10)
Deployment Frequency, Change Failure Rate, MTTR, Lead Time for Changes, Defect Density, Uptime %, Error Rate, p95 Latency, Cost per 1k Requests, Feature Adoption Rate

> Each KPI includes definition, dimensions, SQL patterns, and example business questions.




---

How teams use this library

As a boilerplate: pick a KPI template, map its fields to your warehouse tables/columns, and you’re live.

With agentic systems (Yukti/Chatka): load YAMLs into your metadata store (Firestore/Graph) and let the agent pick dimensions, generate SQL, and explain results.

For demos & sandboxes: load seed CSVs into BigQuery and render instant charts.



---

Mapping to your vocabulary

Every org calls things differently (“CFC” vs “Warehouse”, “Spoke” vs “Drop Zone”).
We recommend maintaining a small mapping file (or knowledge-graph edges) that align your column names and synonyms to template dimensions. Your agent can use that mapping to generalize across clients.


---

Contributing

We welcome PRs for:

New KPIs or additional domains

Better seed data and tests

Corrections to descriptions or SQL patterns


Checklist for PRs

Validate YAML against schema/kpi_schema.json

Include at least one seed CSV row if you add a new template

Keep SQL dialect to BigQuery for now (we’ll add others later)



---

Roadmap

More domains (Sales, Support, Manufacturing)

dbt models to auto-generate metric views from YAML

Optional Graph export (nodes/edges) for knowledge-graph ingestion

Additional SQL dialects (Snowflake, Redshift/Spectrum, DuckDB)

Benchmarks & unit tests for formula correctness



---

License & attribution

Templates and seeds are synthetic and provided under Apache-2.0 (or MIT—choose one).

Please attribute Chatka (Yukti) if you reuse significant portions.



---

Safety & privacy

This repo contains only synthetic data and generic KPI logic.
Do not commit any proprietary schemas, secrets, or real customer data.


---

Contact

Questions or enterprise use?
hello@chatka.co.uk • contact@chatka.co.uk


---

