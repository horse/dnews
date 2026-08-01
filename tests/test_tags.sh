#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

EDITION_DATE="${EDITION_DATE:-$(python - <<'PY'
from pathlib import Path
import sys
sys.path.insert(0, str(Path('tools').resolve()))
from edition import latest_edition_date
print(latest_edition_date(Path('.').resolve()))
PY
)}"

python tools/validate_edition.py --edition-date "$EDITION_DATE"

if [[ "${SKIP_BUILD:-0}" != "1" ]]; then
  bundle exec jekyll build
fi

python - "$EDITION_DATE" <<'PY'
from pathlib import Path
import sys

edition_date = sys.argv[1]
root = Path('.').resolve()
sys.path.insert(0, str((root / 'tools').resolve()))
from edition import collect_posts

site = root / '_site'
required = [
    site / 'index.html',
    site / 'daily' / edition_date / 'index.html',
    site / 'tags' / 'index.html',
]
for path in required:
    if not path.exists():
        raise SystemExit(f'Missing rendered page: {path}')

posts = collect_posts(root, 'zh', edition_date)
for section in ('core', 'social', 'other'):
    post = next(item for item in posts if item.data['daily_section'] == section)
    permalink = str(post.data.get('permalink') or '').strip('/')
    if not permalink:
        raise SystemExit(f'Missing permalink: {post.path}')
    rendered = site / permalink / 'index.html'
    if not rendered.exists():
        raise SystemExit(f'Missing rendered article: {rendered}')

home = (site / 'index.html').read_text(encoding='utf-8')
daily = (site / 'daily' / edition_date / 'index.html').read_text(encoding='utf-8')
for text in ('政治经济与重大事件', '社会观察', '科学、文化、城市与其他'):
    if text not in daily:
        raise SystemExit(f'Daily page missing section: {text}')
if f'/daily/{edition_date}/' not in home:
    raise SystemExit('Homepage does not link to latest daily edition')
if (site / 'japanese').exists():
    raise SystemExit('Japanese WordPress sources must not be published by GitHub Pages')
print(f'Edition acceptance checks passed: {edition_date}')
PY
