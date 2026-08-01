#!/usr/bin/env bash
set -euo pipefail

if [[ "${SKIP_BUILD:-0}" != "1" ]]; then
  bundle exec jekyll build
fi

homepage="_site/index.html"
daily_page="_site/daily/2026-07-31/index.html"
tag_page="_site/tags/index.html"
article_page="_site/news/2026/07/31/kumamoto-earthquake-supply-chain/index.html"

for page in "$homepage" "$daily_page" "$tag_page" "$article_page"; do
  test -f "$page" || {
    echo "Missing rendered page: $page" >&2
    exit 1
  }
done

grep -q 'class="tag-pill"' "$homepage"
grep -q 'class="tag-pill"' "$daily_page"
grep -q '相关标签' "$article_page"
grep -q 'class="tag-pill"' "$article_page"
grep -q '日本气象厅' "$article_page"
grep -q '熊本县' "$tag_page"
grep -q 'kumamoto-earthquake-supply-chain' "$tag_page"

ruby <<'RUBY'
require 'yaml'

Dir['_posts/*.md'].sort.each do |path|
  text = File.read(path, encoding: 'UTF-8')
  parts = text.split(/^---\s*$\n?/, 3)
  abort "#{path}: invalid front matter" unless parts.length == 3

  data = YAML.safe_load(parts[1], aliases: true)
  tags = Array(data['tags'])
  body = parts[2]

  unless (12..25).cover?(tags.length)
    abort "#{path}: expected 12-25 tags, got #{tags.length}"
  end

  missing = tags.reject { |tag| body.include?(tag.to_s) }
  unless missing.empty?
    abort "#{path}: tags absent from body: #{missing.join(', ')}"
  end

  wordpress_tags = Array(data.dig('wordpress', 'tags'))
  unless wordpress_tags == tags
    abort "#{path}: wordpress.tags does not match tags"
  end
end
RUBY

echo "Tag navigation acceptance checks passed."
