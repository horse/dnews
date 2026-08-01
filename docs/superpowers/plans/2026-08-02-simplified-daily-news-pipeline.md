# Simplified Daily News Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace fixed 8/8/10 edition validation with source-defined, flexible 6–8/8–12/10–15 bilingual editions while preserving incremental GitHub Pages and WordPress publishing.

**Architecture:** Keep the existing post formats and publishing workflows. Move flexible count policy into `tools/edition.py`, store actual counts in schema version 3 manifests, generate both daily indexes from those counts, and retain fixed-count compatibility for schema versions 1 and 2.

**Tech Stack:** Python 3.12, PyYAML, unittest, Ruby wrapper, Bash/Jekyll CI, GitHub Pages, WordPress REST workflow.

## Global Constraints

- Coverage window is previous day 06:00:00 through current day 05:59:59 JST.
- Sources are Yahoo!ニュース main pages, Google News Japan top stories, NHK NEWS WEB, 朝日, 読売, 毎日, 日経, 産経, 共同, 時事 and NHK.
- New edition ranges are core 6–8, social 8–12, other 10–15, total 24–35.
- Chinese and Japanese slug sets must match exactly.
- Historical editions remain valid and are never overwritten by a later edition.
- WordPress remains slug-idempotent and GitHub Pages remains append-only by date.

---

### Task 1: Add flexible-count tests

**Files:**
- Modify: `tests/test_edition.py`

**Interfaces:**
- Consumes: `write_generated_edition`, `validate_edition`, `render_japanese_daily`.
- Produces: tests for actual manifest counts, range rejection, dynamic link counts and legacy compatibility.

- [ ] Add a 7/10/13 fixture and assert 30 Chinese posts, 30 Japanese posts and matching manifest counts.
- [ ] Add a 5/10/13 fixture and assert generation fails because core is below range.
- [ ] Assert the Japanese daily contains exactly the actual number of article links.
- [ ] Run `python -m unittest tests/test_edition.py -v` and confirm the new tests fail before implementation.

### Task 2: Implement schema version 3 counts

**Files:**
- Modify: `tools/edition.py`

**Interfaces:**
- Produces: `SECTION_COUNT_RANGES`, dynamic daily renderers, schema version 3 manifests and range-aware validation.

- [ ] Define section ranges and a helper that validates actual counts.
- [ ] Generate Chinese and Japanese daily metadata from actual counts.
- [ ] Build schema version 3 manifests with actual `expected_counts` and `count_ranges`.
- [ ] Validate schema versions 1–2 against legacy 8/8/10 and schema version 3 against flexible ranges.
- [ ] Validate manifest post count, bilingual post count and daily links against the actual total.
- [ ] Run `python -m unittest tests/test_edition.py -v` and confirm all tests pass.

### Task 3: Align editorial and operating documents

**Files:**
- Modify: `docs/daily-automation-runbook.md`
- Modify: `docs/editorial-guide.md`
- Modify: `README.md`
- Modify: `japanese/README.md`
- Modify: `wordpress/README.md`

**Interfaces:**
- Produces: one consistent four-step operating definition and source list.

- [ ] Replace broad radar language with the fixed discovery sources.
- [ ] Document page position and independent repetition as primary ranking signals.
- [ ] Replace fixed 26 and 8/8/10 language with flexible ranges.
- [ ] State that all categories receive equal reporting effort and that both publication paths append rather than replace.

### Task 4: Verify repository and CI compatibility

**Files:**
- Test: `tests/test_edition.py`
- Test: `tests/test_publish_wordpress.py`
- Test: `tests/test_japanese_edition.rb`
- Test: `tests/test_tags.sh`

**Interfaces:**
- Produces: evidence that historical editions and current publishing workflows still pass.

- [ ] Run `python -m unittest tests/test_edition.py tests/test_publish_wordpress.py -v`.
- [ ] Run `python tools/validate_edition.py --all`.
- [ ] Run `python -m py_compile tools/*.py`.
- [ ] Run `bash -n tests/test_tags.sh` and `ruby -c tests/test_japanese_edition.rb`.
- [ ] Create a PR and require bilingual CI and Japanese WordPress CI to pass before merging.