#!/usr/bin/env ruby
# frozen_string_literal: true

require 'yaml'
require 'set'

ROOT = File.expand_path('..', __dir__)
JAPANESE_POSTS = File.join(ROOT, 'japanese', 'posts', '*.md')
CHINESE_POSTS = File.join(ROOT, '_posts', '*.md')
MANIFEST_PATH = File.join(ROOT, 'japanese', 'edition-2026-07-31.yml')
DAILY_PATH = File.join(ROOT, 'japanese', 'daily', '2026-07-31.md')

REQUIRED_FIELDS = %w[
  story_id lang editorial_origin translation_status publication_target title date
  news_date daily_section slug excerpt categories tags article_type analysis_angle
  importance seo_title meta_description source_checked_at wordpress
].freeze
EXPECTED_COUNTS = { 'core' => 8, 'social' => 8, 'other' => 10 }.freeze
MIN_PROSE = { 'core' => 900, 'social' => 700, 'other' => 500 }.freeze

def parse_markdown(path)
  text = File.read(path, encoding: 'UTF-8')
  parts = text.split(/^---\s*$\n?/, 3)
  raise "#{path}: invalid front matter" unless parts.length == 3

  [YAML.safe_load(parts[1], aliases: true), parts[2], parts[1]]
rescue Psych::SyntaxError => e
  raise "#{path}: YAML error: #{e.message.lines.first.strip}"
end

errors = []
japanese_paths = Dir[JAPANESE_POSTS].sort
errors << "expected 26 Japanese posts, got #{japanese_paths.length}" unless japanese_paths.length == 26

counts = Hash.new(0)
japanese_slugs = Set.new
japanese_story_ids = Set.new
japanese_titles = []

japanese_paths.each do |path|
  begin
    data, body, raw_front_matter = parse_markdown(path)
  rescue StandardError => e
    errors << e.message
    next
  end

  missing_fields = REQUIRED_FIELDS.reject { |field| data.key?(field) }
  errors << "#{path}: missing fields: #{missing_fields.join(', ')}" unless missing_fields.empty?

  errors << "#{path}: lang must be ja" unless data['lang'] == 'ja'
  errors << "#{path}: editorial_origin must be japanese-sources" unless data['editorial_origin'] == 'japanese-sources'
  errors << "#{path}: translation_status must be original" unless data['translation_status'] == 'original'
  errors << "#{path}: publication_target must be wordpress" unless data['publication_target'] == 'wordpress'
  errors << "#{path}: news_date must be 2026-07-31" unless data['news_date'].to_s == '2026-07-31'

  section = data['daily_section'].to_s
  errors << "#{path}: invalid daily_section #{section.inspect}" unless EXPECTED_COUNTS.key?(section)
  counts[section] += 1

  slug = data['slug'].to_s
  story_id = data['story_id'].to_s
  errors << "#{path}: duplicate slug #{slug}" if japanese_slugs.include?(slug)
  errors << "#{path}: duplicate story_id #{story_id}" if japanese_story_ids.include?(story_id)
  errors << "#{path}: story_id must end with slug" unless story_id == "2026-07-31-#{slug}"
  japanese_slugs << slug
  japanese_story_ids << story_id
  japanese_titles << data['title'].to_s

  tags = Array(data['tags'])
  categories = Array(data['categories'])
  errors << "#{path}: expected 12-25 tags, got #{tags.length}" unless (12..25).cover?(tags.length)
  errors << "#{path}: expected at least 2 categories" unless categories.length >= 2

  absent_tags = tags.reject { |tag| body.include?(tag.to_s) }
  errors << "#{path}: tags absent from body: #{absent_tags.join(', ')}" unless absent_tags.empty?

  wordpress = data['wordpress'] || {}
  errors << "#{path}: wordpress.status must be draft" unless wordpress['status'] == 'draft'
  errors << "#{path}: wordpress.post_type must be post" unless wordpress['post_type'] == 'post'
  errors << "#{path}: wordpress.comment_status must be closed" unless wordpress['comment_status'] == 'closed'
  errors << "#{path}: wordpress.categories mismatch" unless Array(wordpress['categories']) == categories
  errors << "#{path}: wordpress.tags mismatch" unless Array(wordpress['tags']) == tags

  errors << "#{path}: YAML aliases are not allowed" if raw_front_matter.match?(/(?:&id\d+|\*id\d+)/)
  errors << "#{path}: missing source section" unless body.include?('## 参照資料')
  source_count = body.scan(/^\- \[[^\]]+\]\(https?:\/\/[^\)]+\)$/).length
  errors << "#{path}: expected at least one linked source" if source_count.zero?

  prose = body.split('## 参照資料', 2).first.gsub(/\s/, '')
  min_length = MIN_PROSE.fetch(section, 500)
  errors << "#{path}: prose too short (#{prose.length} < #{min_length})" if prose.length < min_length
end

errors << "section counts mismatch: expected #{EXPECTED_COUNTS.inspect}, got #{counts.inspect}" unless counts == EXPECTED_COUNTS

chinese_slugs = Set.new
Dir[CHINESE_POSTS].sort.each do |path|
  begin
    data, = parse_markdown(path)
  rescue StandardError => e
    errors << e.message
    next
  end
  chinese_slugs << data['slug'].to_s if data['news_date'].to_s == '2026-07-31'
end
errors << "Chinese/Japanese slug sets differ: missing=#{(chinese_slugs - japanese_slugs).to_a.sort.inspect}, extra=#{(japanese_slugs - chinese_slugs).to_a.sort.inspect}" unless chinese_slugs == japanese_slugs

begin
  manifest = YAML.safe_load_file(MANIFEST_PATH, aliases: true)
  errors << 'manifest expected_counts mismatch' unless manifest['expected_counts'] == EXPECTED_COUNTS
  manifest_posts = Array(manifest['posts'])
  errors << "manifest expected 26 posts, got #{manifest_posts.length}" unless manifest_posts.length == 26
  manifest_slugs = manifest_posts.map { |item| item['slug'].to_s }.to_set
  errors << 'manifest slug set differs from Japanese posts' unless manifest_slugs == japanese_slugs
  sorted_importance = manifest_posts.map { |item| item['importance'].to_i }
  errors << 'manifest posts are not ordered by importance' unless sorted_importance == sorted_importance.sort
rescue StandardError => e
  errors << "manifest error: #{e.message}"
end

begin
  daily_data, daily_body, = parse_markdown(DAILY_PATH)
  errors << 'daily lang must be ja' unless daily_data['lang'] == 'ja'
  errors << 'daily WordPress status must be draft' unless daily_data.dig('wordpress', 'status') == 'draft'
  japanese_titles.each do |title|
    errors << "daily index missing title: #{title}" unless daily_body.include?(title)
  end
rescue StandardError => e
  errors << e.message
end

unless errors.empty?
  warn errors.join("\n")
  exit 1
end

puts "Japanese edition checks passed: #{japanese_paths.length} posts, #{counts.inspect}."
