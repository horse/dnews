#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from edition import EditionError, validate_edition, write_generated_edition


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate manifest and daily index files for one bilingual edition.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--edition-date", required=True)
    parser.add_argument("--coverage-start", required=True)
    parser.add_argument("--coverage-end", required=True)
    parser.add_argument("--published-at", required=True)
    parser.add_argument("--wordpress-status", choices=("publish", "draft"), default="publish")
    args = parser.parse_args()
    try:
        paths = write_generated_edition(
            root=Path(args.root).resolve(),
            edition_date=args.edition_date,
            coverage_start=args.coverage_start,
            coverage_end=args.coverage_end,
            published_at=args.published_at,
            wordpress_status=args.wordpress_status,
        )
    except EditionError as exc:
        parser.error(str(exc))
    report = validate_edition(Path(args.root).resolve(), args.edition_date)
    print(json.dumps({"paths": {key: str(path) for key, path in paths.items()}, "validation": report}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
