# AI-Research-Knowledge-Base
For AI research Papers. Building a Knowledge graph and be able to expand on the code

## Layout

- `papers/` — downloaded arXiv PDFs, named `<arxiv_id>_<slugified-title>.pdf`, plus `manifest.json` with title/authors/published date/source URLs for each one.
- `data/arxiv_ids.txt` — the list of arXiv IDs to fetch. Add new IDs here (one per line, `#` comments allowed) to grow the collection.
- `scripts/fetch_arxiv.py` — downloads any IDs in `data/arxiv_ids.txt` that aren't already in `papers/manifest.json`. Re-running it is safe; it skips what's already fetched.
  ```bash
  python3 scripts/fetch_arxiv.py                 # fetch everything new in data/arxiv_ids.txt
  python3 scripts/fetch_arxiv.py --id 2609.06674  # fetch one extra paper ad hoc
  ```
- `.claude/skills/arxiv-fetch/` — a Claude Code skill wrapping the same workflow for future sessions.
