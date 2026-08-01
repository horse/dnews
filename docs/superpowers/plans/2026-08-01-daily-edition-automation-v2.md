# Daily Bilingual Edition Automation V2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make one 06:00 task reliably produce and publish a 26-event Chinese/Japanese morning edition without hard-coded dates or partial main-branch releases.

**Architecture:** Add a manifest-driven edition library that generates indexes and validates one date at a time. CI gates a feature branch before merge; post-merge workflows deploy Chinese Pages and publish only the changed Japanese edition to WordPress.

**Tech Stack:** Python 3.12, PyYAML, Markdown, requests, Ruby/Jekyll, GitHub Actions, WordPress REST API.

## Global Constraints

- 26 events per edition: 8 core, 8 social, 10 other.
- Candidate pool contains news and official releases only.
- Chinese and Japanese slug sets must match exactly.
- WordPress final status defaults to publish.
- No credentials in repository files or logs.

---

### Task 1: Dynamic edition model

**Files:**
- Create: `tools/edition.py`
- Test: `tests/test_edition.py`

- [x] Write failing tests for date discovery, per-date post selection, changed-date parsing and 26-link Japanese daily rendering.
- [x] Run tests and confirm missing module failure.
- [x] Implement edition parsing, generation and validation.
- [x] Run tests and confirm all pass.

### Task 2: Edition generator and validator CLIs

**Files:**
- Create: `tools/build_edition.py`
- Create: `tools/validate_edition.py`
- Modify: `tests/test_japanese_edition.rb`
- Modify: `tests/test_tags.sh`

- [x] Generate manifest and both daily pages from 52 completed article files.
- [x] Validate current or all manifest dates without counting unrelated historical posts.
- [x] Keep compatibility wrappers for existing workflows.

### Task 3: Edition-scoped WordPress publishing

**Files:**
- Modify: `tools/publish_wordpress.py`
- Modify: `tests/test_publish_wordpress.py`
- Modify: `.github/workflows/publish-japanese-wordpress.yml`

- [x] Add failing tests for publish default and edition-scoped path selection.
- [x] Implement direct create/update with publish default and transient retry.
- [x] Detect changed edition dates and publish only 26 posts plus one daily page per edition.
- [x] Verify public URLs and daily links after REST publication.

### Task 4: CI and Pages gating

**Files:**
- Modify: `.github/workflows/tags-ci.yml`
- Modify: `.github/workflows/japanese-ci.yml`
- Modify: `.github/workflows/pages.yml`
- Modify: `index.md`

- [x] Run unit and edition validation before Jekyll build.
- [x] Make the homepage select the latest edition dynamically.
- [x] Prevent Pages deployment when bilingual validation fails.

### Task 5: Operating documentation and scheduler

**Files:**
- Modify: `README.md`
- Modify: `docs/editorial-guide.md`
- Create: `docs/daily-automation-runbook.md`
- Modify: `japanese/README.md`
- Modify: `japanese/WORDPRESS.md`
- Modify: `wordpress/README.md`

- [x] Document the 06:00 rolling window, news-only candidate pool, 26-event selection and dual publication.
- [ ] Update the scheduled task to follow the runbook, use an isolated branch and report only verified publication.
