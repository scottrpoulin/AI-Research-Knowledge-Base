---
name: arxiv-fetch
description: Download arXiv paper PDFs (by ID or arxiv.org URL) into this repo's papers/ directory and record metadata in papers/manifest.json. Use when the user pastes arXiv links/IDs and wants the PDFs saved into this knowledge base, or wants to add more papers to it later.
---

# arXiv Fetch

Downloads PDFs from arxiv.org into `papers/` and keeps `papers/manifest.json`
updated with title/authors/published date/source URLs for each paper. Safe
to re-run: already-downloaded papers are skipped unless `--force` is passed.

## Workflow

1. **Collect IDs.** Extract bare arXiv IDs (`YYMM.NNNNN`, no version suffix)
   from whatever the user pasted (abs links, pdf links, or plain IDs). Append
   any new ones to `data/arxiv_ids.txt` (one per line, `#` comments allowed),
   de-duplicating against what's already there.
2. **Run the fetch script** from the repo root:
   ```bash
   python3 scripts/fetch_arxiv.py
   ```
   To fetch one-off IDs without editing the list file:
   ```bash
   python3 scripts/fetch_arxiv.py --id 2609.06674 --id 2609.04681
   ```
3. **Report results.** The script prints a summary line
   (`downloaded=N skipped=N failed=N`) and lists any failed IDs — retry those
   individually or flag them to the user (paper may be withdrawn, ID typo,
   or arXiv rate-limiting).
4. Do not commit unless the user explicitly asks.

## Notes

- The script paces requests (default 3s) to stay polite to arXiv's API and
  PDF servers — do not remove the pause or parallelize downloads.
- `papers/manifest.json` is the source of truth for what's already fetched;
  it's keyed by arXiv ID so it merges cleanly as the list grows.
- Filenames are `<arxiv_id>_<slugified-title>.pdf`.
