# Composio 100-App Toolkit Research

**Submission:** evidence-led feasibility research into 100 app integrations—API surface, authentication, developer credential access, MCP availability, and practical toolkit buildability.

## Start here

- **Interactive case study:** [Open the report](https://manasvi-1.github.io/composio-100-apps-agent-toolkit-research/) *(enable GitHub Pages once in repository Settings → Pages → Build and deployment → Source: GitHub Actions; until then, view [site/index.html](site/index.html) in the repo.)*
- **Complete 100-app dataset:** [JSON](data/apps.json) · [CSV](data/apps.csv)
- **Evidence/audit records:** [13-app source-review ledger](audit/sample_review.json) · [8 targeted official-source checks](audit/crosscheck.json) · [blind-prior comparison](audit/prior_comparison.json) · [run log](audit/run_log.md)
- **Research pipeline:** [agent](src/research_agent.py) · [validator](src/validate.py) · [sample-review arithmetic check](src/verify_sample.py) · [report builder](src/build_report.py)

## Executive readout

The submitted inventory has **100 app records across 10 balanced categories**, with **198 source URL references**. The descriptive patterns in the report are calculated from those records. They are a snapshot of the supplied transcript—not a claim about the entire current Composio catalog.

The evidence review covers a selected 13-app sample (78 field claims), plus eight targeted first-party checks. This is an assistant-assisted source review, not independent human sign-off or a statistically representative accuracy benchmark. The blind-prior comparison scores **68/90 fields against transcript labels**; that is label concordance, not factual accuracy.

## Provenance and limitations — read before interpreting the numbers

The 100 structured app records were extracted from the Qwen research transcript provided for this project. They were **not freshly researched from scratch for all 100 apps in this repository run**. The transcript preserved source URLs and confidence labels, but not per-URL retrieval timestamps or field-level claim mappings. A URL attached to a row does not prove every field is supported by that URL.

This repository adds normalization, deterministic checks, report generation, reproducibility artifacts, and targeted first-party-source checks. It does not claim:
- that all 198 URLs were opened and claim-audited;
- that a live Composio SDK/catalog call or provider credential flow was tested;
- that every integration was executed against its upstream API;
- that the assistant's selected source-review sample is independent human verification.

The report intentionally separates recorded labels, source-supported checks, corrections, and unresolved claims.

## Reproduce the local checks

Python 3.10+; core validation/report code uses the standard library.

```bash
python src/validate.py
python src/verify_sample.py --write
python src/reproduce_prior_comparison.py
python src/build_report.py
python -m unittest discover -s tests -v
```

The report builder writes a self-contained HTML report and stages its linked JSON/CSV/audit artifacts under `site/` for static hosting.

## Run the live research agent (optional; API usage may incur charges)

The research runner requires an Exa search key and an OpenAI-compatible API key. Configure them in your shell or a local `.env` that is **not committed**:

```powershell
$env:EXA_API_KEY="..."
$env:OPENAI_API_KEY="..."
$env:OPENAI_MODEL="gpt-4.1-mini" # or a model supported by your provider
python src/research_agent.py --dry-run --limit 3
python src/research_agent.py --limit 3
```

After validating a small run, continue in resumable batches by setting `--start` and `--limit`. Output is JSONL and records raw search snippets, retrieval timestamps, model findings, and review-required status. The runner does not silently replace failures with invented results. **Do not upload API keys to GitHub or paste them into chat.** A Qwen/ChatGPT subscription upgrade is not required for this repository's static submission; provider API credentials and usage billing are separate.

## Research interpretation

A vendor API existing is not equivalent to a toolkit being shippable. Credential issuance, account role, scopes, app review, sandbox availability, contracts, and tenant policy can be the decisive blocker. MCP classification must identify the exact server/toolkit: provider-hosted MCP and Composio-built toolkits can differ in auth and tool coverage.

## Submission

This public repository is the single source of truth: **[GitHub repository](https://github.com/Manasvi-1/composio-100-apps-agent-toolkit-research)**. The report, dataset, audit trail, and code are linked above. No claims of complete independent 100-app verification are made.
