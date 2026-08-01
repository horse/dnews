#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from edition import EditionError, discover_edition_dates, latest_edition_date, validate_edition


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate one or all bilingual dnews editions.")
    parser.add_argument("--root", default=".")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--edition-date")
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    dates = discover_edition_dates(root) if args.all else [args.edition_date or latest_edition_date(root)]
    reports = []
    try:
        for date in dates:
            reports.append(validate_edition(root, date))
    except EditionError as exc:
        print(str(exc))
        return 1
    print(json.dumps({"validated": reports}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
