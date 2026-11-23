# Dataset and provenance

- `apps.json` and `apps.csv` contain the normalized 100-app candidate inventory.
- The records are transcript-extracted from the user's supplied Qwen research, not a new independently executed 100-app pass.
- The 198 evidence URL references were retained, but not every URL was opened and claim-audited.
- Source-review results and targeted official checks are in `../audit/sample_review.json` and `../audit/crosscheck.json`.
- Treat classifications as candidate labels unless the corresponding claim has a scoped source review.
- Do not interpret blind-prior concordance as factual accuracy.

Rebuild and validate with the commands in the root README.
