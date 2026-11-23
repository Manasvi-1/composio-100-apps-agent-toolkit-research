# Composio 100-App Toolkit Research

Evidence-led assessment of 100 app integrations: authentication, credential acquisition, API surface, MCP/toolkit type, and practical buildability.

## Evidence audit in progress

The initial public commit was a scaffold. This update records substantive work against the Qwen transcript supplied by the user and official-source checks performed in this session.

**Provenance:** the 100 app-level records are extracted from the supplied Qwen transcript, not represented as fresh 100-app research independently conducted by this repo. The transcript contains 198 source URLs and a 20-app blind prior sample. It does not preserve retrieval timestamp/source tier per URL.

## Reproducibility and evidence

- 100 records, ten categories × ten apps.
- 198 source URL references; presence of a URL is not proof every claim is correct.
- Eight targeted app claims cross-checked against first-party documentation; exact scope and URLs in audit/crosscheck.json.
- Prior comparison in audit/prior_comparison.json: 68/90 fields agree with transcript labels after mapping NotebookLM to NotebookLM (Gemini Notebook). This is NOT independent factual accuracy.
- Deterministic checks cover row count, IDs, category balance, required fields, and URL shape—not truth.

## Composio architecture detail

An app may group multiple distinct toolkits, including Composio-built API toolkits and provider-hosted MCP toolkits. They can differ in auth, tool coverage, and connections. Classify exact toolkit/server, not just product name or _mcp suffix.

Official docs:
- https://docs.composio.dev/docs/apps-and-toolkits
- https://docs.composio.dev/docs/apps-and-toolkits/provider-mcps
- https://docs.composio.dev/docs/apps-and-toolkits/composio-built-vs-provider-mcp

## Run

python src/validate.py
python src/reproduce_prior_comparison.py

The original research runner is a configurable search + structured extraction pipeline and requires external search/LLM credentials. It was NOT executed in this run. No Composio SDK call or credentialed integration test was performed. Do not claim the complete research pipeline was rerun end-to-end.

## Remaining gates

1. Publish the complete normalized 100-row dataset and generated interactive report to this repository.
2. Add per-source retrieval dates, source types, and field-level claim-to-evidence mappings.
3. Re-open all 198 source URLs and validate claims, prioritizing low-confidence, gated, and MCP fields.
4. Repair and independently ground blind-sample comparison before reporting accuracy.
5. Run the research agent with declared provider settings and archive retrieval outputs; check Composio catalog separately from upstream API access.

This is a candid interim evidence update—not a finished take-home.
