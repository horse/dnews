#!/usr/bin/env bash
set -euo pipefail

if [[ "${SKIP_BUILD:-0}" != "1" ]]; then
  bundle exec jekyll build
fi

homepage="_site/index.html"
daily_page="_site/daily/2026-07-31/index.html"
tag_page="_site/tags/index.html"
core_page="_site/news/2026/07/31/kumamoto-earthquake-supply-chain/index.html"
social_page="_site/news/2026/07/31/kumamoto-water-heat-evacuation/index.html"
other_page="_site/news/2026/07/31/kahaku-human-earth-exhibition/index.html"

for page in "$homepage" "$daily_page" "$tag_page" "$core_page" "$social_page" "$other_page"; do
  test -f "$page" || { echo "Missing rendered page: $page" >&2; exit 1; }
done

grep -q '政治经济大事' "$homepage"
grep -q '社会观察' "$homepage"
grep -q '日本的其他现场' "$homepage"
grep -q '政治经济大事' "$daily_page"
grep -q '社会观察' "$daily_page"
grep -q '科学、文化、城市与其他' "$daily_page"
grep -q 'class="social-grid"' "$daily_page"
grep -q 'class="brief-grid"' "$daily_page"
grep -q '相关标签' "$core_page"
grep -q '相关标签' "$social_page"
grep -q '相关标签' "$other_page"
grep -q 'kumamoto-water-heat-evacuation' "$tag_page"
grep -q 'kahaku-human-earth-exhibition' "$tag_page"

ruby <<'RUBY'
require 'yaml'

counts = Hash.new(0)
allowed = %w[core social other]
errors = []

Dir['_posts/*.md'].sort.each do |path|
  text = File.read(path, encoding: 'UTF-8')
  parts = text.split(/^---\s*$\n?/, 3)
  if parts.length != 3
    errors << "#{path}: invalid front matter"
    next
  end

  begin
    data = YAML.safe_load(parts[1], aliases: true)
  rescue Psych::SyntaxError => error
    errors << "#{path}: YAML error: #{error.message.lines.first.strip}"
    next
  end

  tags = Array(data['tags'])
  body = parts[2]
  section = data['daily_section'].to_s

  errors << "#{path}: invalid daily_section #{section.inspect}" unless allowed.include?(section)
  errors << "#{path}: expected 12-25 tags, got #{tags.length}" unless (12..25).cover?(tags.length)

  missing = tags.reject { |tag| body.include?(tag.to_s) }
  errors << "#{path}: tags absent from body: #{missing.join(', ')}" unless missing.empty?

  wordpress_tags = Array(data.dig('wordpress', 'tags'))
  errors << "#{path}: wordpress.tags does not match tags" unless wordpress_tags == tags

  counts[section] += 1 if data['news_date'].to_s == '2026-07-31'
end

expected = {'core' => 8, 'social' => 8, 'other' => 10}
errors << "section counts mismatch: expected #{expected.inspect}, got #{counts.inspect}" unless counts == expected

unless errors.empty?
  warn errors.join("\n")
  exit 1
end
RUBY

echo "Expanded daily edition acceptance checks passed."
