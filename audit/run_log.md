# Run log — 2026-11-23

## Input provenance
- Assignment: research 100 apps for auth/access, API, MCP, buildability, patterns, agent pipeline, verification, report and public repo.
- Qwen transcript is the source for the 100 structured app records. I extracted its embedded Python literal data via AST-safe literal parsing, preserving URLs, confidence labels and flags.
- Blind prior lock: 2026-11-23T14:41:15.656809Z; 20 apps; SHA-256 4571ce6394e5d2c20a910e2209d93d73eb977799ced596ade1774513fc6a3811.

## Work completed in this iteration
- Parsed 100 records; IDs 1..100; ten categories × ten apps.
- Preserved 198 source URL references.
- Added eight claim-scoped official-source checks: Salesforce, DealCloud, LinkedIn Ads, Pylon, Brex, Snowflake, Neo4j Aura, HubSpot.
- Replayed blind-prior comparison. Transcript code had app-name mismatch NotebookLM vs NotebookLM (Gemini Notebook). Explicit alias repairs the comparison: 68/90 non-excluded fields agree with transcript labels; 22 differ. This is label concordance, NOT factual accuracy.
- Deterministic validation: 100 records, unique app names, balanced categories, required fields, 198 URL references, zero structural errors.
- Generated a local searchable/filterable HTML report.

## Not executed
- No fresh 100-app research pass in this session.
- No paid search/LLM API calls.
- No Composio SDK or live catalog call; credentials/runtime not available.
- Not all 198 evidence URLs opened individually.
- Full dataset/report publication and Pages deployment remain pending verification.

## Corrections and methodological notes
- App and toolkit are not synonymous; Composio docs distinguish Composio-built and provider-hosted MCP toolkits, which can differ in auth/tools/connections.
- Free API/sandbox does not guarantee production credential self-service; admin roles, scopes, app review, contract/license and tenant policy matter.
- “No MCP” means not found within a bounded official-source check, not universal absence.
