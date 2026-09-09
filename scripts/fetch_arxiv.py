#!/usr/bin/env python3
"""Download arXiv PDFs and record metadata for the knowledge base.

Reads arXiv IDs from a text file (default: data/arxiv_ids.txt), fetches
title/authors/date from the arXiv API, downloads each PDF into papers/,
and maintains a JSON manifest (papers/manifest.json) so re-runs are
idempotent and skip files that are already present.

Usage:
    python scripts/fetch_arxiv.py
    python scripts/fetch_arxiv.py --ids-file data/arxiv_ids.txt --out-dir papers
    python scripts/fetch_arxiv.py --id 2609.06674          # single ad-hoc fetch
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import socket
import unicodedata
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

NETWORK_ERRORS = (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError)

ARXIV_ID_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}
USER_AGENT = "ai-research-kb-fetch/1.0 (mailto:scottrpoulin@gmail.com)"


def extract_id(raw: str) -> str | None:
    """Pull a bare arXiv ID (no version suffix) out of an ID or URL string."""
    raw = raw.strip()
    if not raw or raw.startswith("#"):
        return None
    m = ARXIV_ID_RE.search(raw)
    return m.group(1) if m else None


def slugify(title: str, max_len: int = 80) -> str:
    title = unicodedata.normalize("NFKD", title)
    title = title.encode("ascii", "ignore").decode("ascii")
    title = re.sub(r"[^\w\s-]", "", title).strip().lower()
    title = re.sub(r"[\s_]+", "-", title)
    return title[:max_len].strip("-") or "untitled"


def fetch_metadata(ids: list[str], batch_size: int = 20, pause: float = 3.0, retries: int = 3) -> dict[str, dict]:
    """Query the arXiv API in batches, return {id: {title, authors, published}}."""
    results: dict[str, dict] = {}
    for i in range(0, len(ids), batch_size):
        batch = ids[i : i + batch_size]
        url = "http://export.arxiv.org/api/query?id_list=" + ",".join(batch) + f"&max_results={len(batch)}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        data = None
        for attempt in range(1, retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = resp.read()
                break
            except NETWORK_ERRORS as e:
                print(f"  ! metadata fetch attempt {attempt}/{retries} failed for batch {batch}: {e}", file=sys.stderr)
                if attempt < retries:
                    time.sleep(pause)
        if data is None:
            continue

        root = ET.fromstring(data)
        for entry in root.findall("atom:entry", ATOM_NS):
            entry_id = entry.find("atom:id", ATOM_NS).text
            arxiv_id = extract_id(entry_id)
            if not arxiv_id:
                continue
            title = entry.find("atom:title", ATOM_NS).text.strip()
            title = re.sub(r"\s+", " ", title)
            authors = [
                a.find("atom:name", ATOM_NS).text
                for a in entry.findall("atom:author", ATOM_NS)
            ]
            published = entry.find("atom:published", ATOM_NS).text[:10]
            results[arxiv_id] = {"title": title, "authors": authors, "published": published}

        if i + batch_size < len(ids):
            time.sleep(pause)
    return results


def download_pdf(arxiv_id: str, dest: Path, pause: float = 3.0, retries: int = 3) -> bool:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        for attempt in range(1, retries + 1):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    dest.write_bytes(resp.read())
                return True
            except NETWORK_ERRORS as e:
                print(f"  ! download attempt {attempt}/{retries} failed for {arxiv_id}: {e}", file=sys.stderr)
                if attempt < retries:
                    time.sleep(pause)
        return False
    finally:
        time.sleep(pause)


def load_manifest(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {}


def save_manifest(path: Path, manifest: dict) -> None:
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids-file", type=Path, default=Path("data/arxiv_ids.txt"))
    parser.add_argument("--out-dir", type=Path, default=Path("papers"))
    parser.add_argument("--id", action="append", dest="extra_ids", default=[],
                         help="Fetch a single extra arXiv ID (repeatable), in addition to --ids-file.")
    parser.add_argument("--pause", type=float, default=3.0, help="Seconds to wait between arXiv requests.")
    parser.add_argument("--force", action="store_true", help="Re-download even if a PDF already exists.")
    args = parser.parse_args()

    ids: list[str] = []
    if args.ids_file.exists():
        for line in args.ids_file.read_text().splitlines():
            aid = extract_id(line)
            if aid and aid not in ids:
                ids.append(aid)
    for raw in args.extra_ids:
        aid = extract_id(raw)
        if aid and aid not in ids:
            ids.append(aid)

    if not ids:
        print("No arXiv IDs found.", file=sys.stderr)
        sys.exit(1)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.out_dir / "manifest.json"
    manifest = load_manifest(manifest_path)

    to_fetch_meta = [i for i in ids if i not in manifest or args.force]
    print(f"{len(ids)} IDs total, fetching metadata for {len(to_fetch_meta)} new/forced entries...")
    metadata = fetch_metadata(to_fetch_meta, pause=args.pause) if to_fetch_meta else {}

    downloaded, skipped, failed = 0, 0, []
    for aid in ids:
        meta = metadata.get(aid) or manifest.get(aid, {})
        title = meta.get("title", "")
        slug = slugify(title) if title else "untitled"
        filename = f"{aid}_{slug}.pdf" if title else f"{aid}.pdf"
        dest = args.out_dir / filename

        existing_entry = manifest.get(aid)
        if existing_entry and not args.force:
            existing_path = args.out_dir / existing_entry.get("filename", "")
            if existing_path.exists():
                skipped += 1
                continue

        print(f"[{aid}] {title or '(no title found)'}")
        ok = download_pdf(aid, dest, pause=args.pause)
        if not ok:
            failed.append(aid)
            continue

        downloaded += 1
        manifest[aid] = {
            "filename": filename,
            "title": title,
            "authors": meta.get("authors", []),
            "published": meta.get("published", ""),
            "abs_url": f"https://arxiv.org/abs/{aid}",
            "pdf_url": f"https://arxiv.org/pdf/{aid}",
        }
        save_manifest(manifest_path, manifest)  # persist after every file: safe to interrupt/resume

    print(f"\nDone. downloaded={downloaded} skipped(existing)={skipped} failed={len(failed)}")
    if failed:
        print("Failed IDs:", ", ".join(failed))


if __name__ == "__main__":
    main()
