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
core_headings = ('政治经济与重大事件', '政治经济大事')
if not any(text in daily for text in core_headings):
    raise SystemExit(f'Daily page missing core section: {core_headings}')
for text in ('社会观察', '科学、文化、城市与其他'):
    if text not in daily:
        raise SystemExit(f'Daily page missing section: {text}')
if f'/daily/{edition_date}/' not in home:
    raise SystemExit('Homepage does not link to latest daily edition')
if (site / 'japanese').exists():
    raise SystemExit('Japanese WordPress sources must not be published by GitHub Pages')
print(f'Edition acceptance checks passed: {edition_date}')
PY

if [[ "$EDITION_DATE" == "2026-08-02" ]]; then
  urls=(
    "https://horse.github.io/dnews/daily/2026-08-02/"
    "https://shinkiji.com/japan-daily-2026-08-02/"
    "https://shinkiji.com/kumamoto-water-outage-heat/"
    "https://shinkiji.com/kumamoto-first-weekend-recovery/"
    "https://shinkiji.com/tohoku-heavy-rain-level4/"
    "https://shinkiji.com/uki-aftershock-shindo5/"
    "https://shinkiji.com/japan-dangerous-heat-august1/"
    "https://shinkiji.com/kumamoto-aeon-explosion-analysis/"
    "https://shinkiji.com/kumamoto-disaster-related-deaths/"
    "https://shinkiji.com/henoko-capsizing-family-video/"
    "https://shinkiji.com/kumamoto-91yo-collapse-family/"
    "https://shinkiji.com/kumamoto-babies-fukuda-hospital/"
    "https://shinkiji.com/one-child-second-child-wall/"
    "https://shinkiji.com/chiba-explosion-gas-smell/"
    "https://shinkiji.com/okayama-missing-two-year-old-cutoff/"
    "https://shinkiji.com/kumamoto-community-rescue-wife/"
    "https://shinkiji.com/japan-volleyball-usa-semifinal/"
    "https://shinkiji.com/summer-koshien-draw/"
    "https://shinkiji.com/murakami-24th-rookie-record/"
    "https://shinkiji.com/girls-baseball-kobe-koryo-title/"
    "https://shinkiji.com/ohtani-24th-dodgers-loss/"
    "https://shinkiji.com/aiko-toba-aquarium/"
    "https://shinkiji.com/manga-koshien-opens/"
    "https://shinkiji.com/yamada-goro-final-lesson/"
    "https://shinkiji.com/ensemble-stars-stage-response/"
    "https://shinkiji.com/nagaoka-fireworks-manners/"
  )
  for url in "${urls[@]}"; do
    status="$(curl --location --silent --show-error --output /tmp/public-page.html --write-out '%{http_code}' --connect-timeout 15 --max-time 45 --retry 2 --retry-delay 5 "$url")"
    if [[ "$status" != "200" ]]; then
      echo "Public URL failed: $status $url" >&2
      exit 1
    fi
    bytes="$(wc -c < /tmp/public-page.html)"
    if (( bytes < 500 )); then
      echo "Public URL returned too little content: $bytes bytes $url" >&2
      exit 1
    fi
    echo "Public URL OK: $status $bytes $url"
  done
fi
