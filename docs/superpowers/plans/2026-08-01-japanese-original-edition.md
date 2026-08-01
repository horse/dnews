# Japanese Original Edition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 26 Japanese-language original reports for the 2026-07-31 edition without modifying the existing Chinese reports.

**Architecture:** Store Japanese WordPress drafts under `japanese/`, paired to Chinese reports by `story_id` and `slug`. Keep Japanese content out of the Chinese Jekyll build, validate both language sets together, and use an edition manifest as the machine-readable inventory.

**Tech Stack:** Markdown, YAML, Ruby, Jekyll, GitHub Actions, WordPress REST-compatible front matter.

## Global Constraints

- Japanese reports must be written directly from Japanese primary sources and reporting, not translated from Chinese copy.
- Existing Chinese titles, bodies, slugs, permalinks and public pages must remain unchanged.
- The edition contains exactly 8 core, 8 social and 10 other Japanese reports.
- Each Japanese report has 12–25 Japanese tags, all present verbatim in the article body.
- `wordpress.status` remains `draft`; `wordpress.categories` and `wordpress.tags` match top-level values.
- `japanese/` is excluded from the Chinese GitHub Pages build.

---

### Task 1: Create the Japanese content model and manifest
- [x] Create `japanese/README.md`.
- [x] Create `japanese/edition-2026-07-31.yml` with exact counts and all 26 paths.
- [x] Define WordPress-compatible front matter and shared `story_id`/`slug` fields.

### Task 2: Write eight core reports
- [x] Write the earthquake and supply-chain report.
- [x] Write the BOJ policy report.
- [x] Write two yen-intervention reports.
- [x] Write the national-intelligence report.
- [x] Write CPI, labor and industrial-output reports.

### Task 3: Write eight social-observation reports
- [x] Write disaster living-conditions, emergency-care and public-facility reports.
- [x] Write parenting, skilled-trades and museum-accessibility reports.
- [x] Write environmental-policy and Tokyo-opinion-survey reports.

### Task 4: Write ten science, culture, city and other reports
- [x] Write museum, hotel, family-program, literature and local-history reports.
- [x] Write medical-education, medical-physics, cinema, baseball and park reports.

### Task 5: Compose and validate the Japanese edition
- [x] Create `japanese/daily/2026-07-31.md`.
- [x] Add repository validation for counts, metadata, body tags, Chinese pairing and prose length.
- [x] Exclude `japanese/` from the Chinese Jekyll build.
- [ ] Run the complete Japanese validation and existing Chinese Jekyll checks.
- [ ] Review the branch diff and merge after CI succeeds.
