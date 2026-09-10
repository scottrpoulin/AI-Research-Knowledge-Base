---
name: dair-ai-paper-watch
description: Check DAIR.AI's LinkedIn company posts for new paper links (posted in the comments), surface them for review in a live Artifact with Approve/Skip buttons, and sync approved papers into this repo via scripts/add_paper.sh. Use when the user asks to check dair-ai / DAIR.AI on LinkedIn for new papers, or to review/sync the paper queue artifact.
---

# DAIR.AI LinkedIn Paper Watch

Source page: `https://www.linkedin.com/company/dair-ai/posts/?feedView=all`.
DAIR.AI posts about a paper, and the actual paper link is posted as a
**comment** on that post (usually by the page itself), not in the post body.
This requires a logged-in LinkedIn session, so it must run through
**Claude in Chrome** (the user's real, already-authenticated browser) — it
cannot run as a headless/cloud scheduled job. The user runs this manually
whenever they want a check (no cron).

State lives in one place: the **live Artifact itself** (read back with
`Artifact` `action: "read"` at the start of every run — no separate local
state file for pending/approved/skipped/added history). The only local
record is `data/dair_ai_watch.json`, which just remembers the artifact's
`url` so repeated runs update the same page instead of creating a new one.

## Step 1 — Load the browser tools

```
ToolSearch query="select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__tabs_create_mcp"
```

## Step 2 — Find the artifact URL (if one exists)

Read `data/dair_ai_watch.json`. If it has a `url`, call `Artifact action:"read"`
on it first — **before scraping** — and process any items already sitting in
its `approved` array that aren't yet in `added` (see Step 6: this is the
catch-up path for approvals clicked while no session was watching). If the
file doesn't exist yet, this is the first run: skip straight to Step 3 and
publish a fresh artifact at the end.

## Step 3 — Scrape recent posts

Using Claude in Chrome:
1. Navigate to `https://www.linkedin.com/company/dair-ai/posts/?feedView=all`.
2. Read the page / scroll to load the most recent ~10–15 posts. Compare post
   URLs (or LinkedIn's post URN if visible) against the artifact's existing
   `pending` + `added` + `skipped` entries (by `post_url`) to figure out which
   posts are new since the last run — don't reprocess ones already seen.
3. For each new post, open its comments and read them (`get_page_text` on the
   comment section, or click "N comments" first if collapsed).
4. Extract any paper link from the comments — mainly `arxiv.org/abs/...` or
   `arxiv.org/pdf/...`, but capture any other paper URL (e.g. OpenReview,
   ACL Anthology) verbatim even if it's not an arXiv ID. Pull the bare arXiv
   ID with the same `YYMM.NNNNN` pattern used in `data/arxiv_ids.txt`.
5. For arXiv links, you already know how to get title/authors/published date
   — reuse the same `http://export.arxiv.org/api/query?id_list=...` lookup
   pattern from `scripts/fetch_arxiv.py` (or just run
   `python3 scripts/fetch_arxiv.py --id <id>` later at sync time, which fills
   this in automatically — no need to duplicate the metadata fetch here if
   you'd rather keep the queue entry minimal and backfill title on sync).

Be a polite, occasional visitor: this is a manual, user-triggered check, not
a scraper loop — don't hammer LinkedIn with rapid repeated requests.

## Step 4 — Reconcile against the repo

Cross-check every candidate arXiv ID against `papers/manifest.json`. If it's
already there, don't add it to `pending` — it's already in the repo.

## Step 5 — Publish/update the live Artifact

Build the page as described in `reference/artifact_template.md` in this
skill directory: it declares `capabilities: {artifact: {}}`, embeds the
current state as JSON in a `<script id="app-state" type="application/json">`
tag, and renders Pending (with Approve/Skip buttons), Recently Added, and
Recently Skipped sections. Each button click updates state client-side and
calls `artifact.publish(newHtml)` to persist it and notify this (watching)
session.

- First run: `Artifact` `action:"publish"`, pick a title/favicon, then save
  the returned URL into `data/dair_ai_watch.json`.
- Later runs: `Artifact` `action:"publish"` with `url` set to the saved URL,
  merging newly-found `pending` items into whatever the artifact already had
  (don't clobber items a run didn't touch).

Publishing keeps this session subscribed to the artifact's live changes.

## Step 6 — Handle approvals (live, and on catch-up)

When notified that the artifact was republished (or when catching up at the
top of a later run), re-read it and look for entries in `approved` that
aren't yet reflected in `added`:

```bash
scripts/add_paper.sh <arxiv_id> [<arxiv_id> ...]
```

This appends the ID(s) to `data/arxiv_ids.txt` and runs the existing
`scripts/fetch_arxiv.py`, which downloads the PDF and updates
`papers/manifest.json`. After it succeeds, republish the artifact moving
that item from `approved` into `added` (with a timestamp) so the user sees
the confirmation. Tell the user what was added; ask before running `git add`
/ `git commit`, and always ask before `git push` — don't push unattended.

If an entry in `approved` fails to fetch (bad ID, withdrawn paper), leave it
visible with an error note rather than silently dropping it, and surface the
failure to the user in chat.

## Notes / limits

- Real-time push only works while a session that published the artifact is
  still open and watching it. If the user clicks Approve/Skip with no
  session watching, nothing happens until the *next* time this skill runs —
  Step 2's catch-up read handles that, so approvals are never lost, just
  delayed until the next manual check.
- Keep `added`/`skipped` history capped (e.g. last ~30 each) so the artifact
  doesn't grow unbounded; older history can just be dropped, the real
  source of truth for "added" is `papers/manifest.json`.
