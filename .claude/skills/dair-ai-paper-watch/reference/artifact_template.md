# Paper queue artifact — design + template

## Design plan

Subject: a personal triage queue for papers DAIR.AI links to in LinkedIn
comments, reviewed against this repo's `papers/manifest.json`. It's a tool
that gets *operated* (approve/skip), not read top to bottom — dashboard
treatment, not editorial.

- **Color** (name → hex, light theme; dark theme swaps roles, see CSS):
  - `--paper #EFF1EA` — page ground, pale warm sage-grey (not the cream/
    terracotta cliché).
  - `--surface #FFFFFF` — card surfaces.
  - `--ink #1E2A22` / `--ink-muted #5C6B60` — text.
  - `--line #D8DCCF` — hairline rules, card borders.
  - `--accent #1F5C6B` — deep teal-ink brand accent (header, links, the
    DAIR.AI eyebrow). Used for identity, never for good/bad state.
  - `--flag #B8842C` — amber "needs review" flag, distinct role from accent.
  - `--good #3B7A3F` / `--bad #A34A3A` — semantic approve/skip colors,
    intentionally different hue-family from the accent teal.
- **Type**: `Source Serif 4` for headings (ties to the academic-paper
  subject matter), `IBM Plex Sans` for UI/body text, `IBM Plex Mono` for
  arXiv IDs, dates, and counts (tabular figures).
- **Layout**: single centered column (~760px), a header with an eyebrow +
  serif H1 + stat chips (Pending / Added / Skipped, mono numerals), then a
  Pending Review card list (title, meta chip row, source-post link, comment
  snippet, Add/Skip buttons), then compact Recently Added and a collapsed
  Recently Skipped `<details>` section.

## How to fill this template

The whole page is one static HTML file with one `<script type="application/
json" id="app-state">` block holding the real state (see schema below) and
a render function that reads it. To build the real artifact for a run:

1. Copy `template.html` in this directory.
2. Replace the contents of `#app-state` with the real state JSON for this
   run (merge newly-found `pending` items into whatever the artifact
   already had — don't drop existing entries a run didn't touch).
3. Publish it (`Artifact` tool, `capabilities: {artifact: {}}`, first run
   with no `url`, later runs with the saved `url` from
   `data/dair_ai_watch.json`).

### State schema

```jsonc
{
  "generatedAt": "2026-09-09T18:04:00Z",
  "pending": [
    {
      "arxiv_id": "2609.06674",           // or null if not an arXiv link
      "paper_url": "https://arxiv.org/abs/2609.06674",
      "title": "Detokenization Leaks: ...", // "" if not looked up yet
      "authors": ["A. Name", "B. Name"],
      "published": "2026-09-08",
      "post_url": "https://www.linkedin.com/feed/update/urn:li:activity:...",
      "post_snippet": "New paper on cache-trace privacy leaks...",
      "comment_snippet": "Paper: https://arxiv.org/abs/2609.06674",
      "found_at": "2026-09-09T18:04:00Z"
    }
  ],
  "approved": [ /* same shape as pending, plus "approved_at" */ ],
  "added":   [ /* {arxiv_id, title, added_at} — cap ~30, newest first */ ],
  "skipped": [ /* {arxiv_id, title, skipped_at} — cap ~30, newest first */ ]
}
```

`pending` and `approved` should be near-empty in steady state — items move
to `added`/`skipped` as soon as a watching session processes them. Long
sitting `approved` entries just mean no session has been watching; the
skill's catch-up step handles those on the next run.

### Button wiring (already in `template.html`)

```js
async function decide(id, decision) { // decision: "approve" | "skip"
  const item = state.pending.find(p => p.arxiv_id === id || p.post_url === id);
  if (!item) return;
  state.pending = state.pending.filter(p => p !== item);
  if (decision === "approve") {
    state.approved.unshift({ ...item, approved_at: new Date().toISOString() });
  } else {
    state.skipped.unshift({ arxiv_id: item.arxiv_id, title: item.title, skipped_at: new Date().toISOString() });
    state.skipped = state.skipped.slice(0, 30);
  }
  render(); // optimistic local update
  const artifact = await claude.use("artifact");
  if (!artifact) return; // read-only view, nothing to persist
  try {
    await artifact.publish(buildHtml(state));
  } catch (e) {
    // conflict: the shell is already reloading this view to the winner — do nothing.
    // any other code: leave the optimistic UI, it'll reconcile on next reload.
  }
}
```

`buildHtml(state)` is the same function used on initial render — it must
produce the **complete** document (doctype through `</html>`), never a DOM
serialization, per the `artifact` capability's contract.

See `template.html` for the full page (CSS tokens for both themes, card
markup, and this script wired up end to end).
