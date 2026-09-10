#!/usr/bin/env bash
# Add one or more arXiv IDs to data/arxiv_ids.txt and fetch them immediately.
# Idempotent: safe to call with IDs already tracked/downloaded.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <arxiv_id> [arxiv_id ...]" >&2
  exit 1
fi

for id in "$@"; do
  grep -qxF "$id" data/arxiv_ids.txt || echo "$id" >> data/arxiv_ids.txt
done

python3 scripts/fetch_arxiv.py
