# Expanded Daily Edition Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Expand the 2026-07-31 dnews edition from eight core reports to 26 independently reported articles arranged in three editorial layers.

**Architecture:** Keep Markdown front matter as the sole content source. Add a `daily_section` field to each post, query the three sections independently in Liquid, and preserve the existing `importance` sorting convention within each layer. Existing tag and WordPress metadata checks remain mandatory and are extended with section-count and rendered-heading assertions.

**Tech Stack:** Jekyll 3.10, Liquid, Minima 2.5, SCSS, Markdown/YAML, Bash, Ruby YAML, GitHub Actions, GitHub Pages.

## Global Constraints

- Existing eight article bodies, titles, slugs, permalinks and sources must not change.
- `daily_section` must be one of `core`, `social`, `other`.
- The 2026-07-31 edition must contain exactly 8 core, 8 social and 10 other posts.
- Every post must contain 12–25 tags, every tag must occur verbatim in the body, and `wordpress.tags` must exactly match `tags`.
- Every new article must identify a July 31 new fact, opening, result, launch or formal event.
- Public copy must read as news and must not expose production workflow, scoring or engineering language.
- GitHub Pages and WordPress must consume the same Markdown metadata.

---

### Task 1: Add section metadata and failing acceptance checks

**Files:**
- Modify: `_posts/2026-08-01-*.md` for the existing eight posts
- Modify: `tests/test_tags.sh`
- Modify: `.github/workflows/tags-ci.yml`

**Interfaces:**
- Consumes: existing post front matter and rendered Jekyll output.
- Produces: validated `daily_section` values and exact section-count assertions.

- [ ] **Step 1: Add `daily_section: core` to the existing eight posts without changing any other content.**
- [ ] **Step 2: Extend the Ruby test to group posts with `news_date == '2026-07-31'` by `daily_section` and require `{core: 8, social: 8, other: 10}`.**
- [ ] **Step 3: Add rendered checks for the headings `政治经济大事`, `社会观察`, and `科学、文化、城市与其他`.**
- [ ] **Step 4: Run the pull-request CI and verify it fails because social and other posts do not exist yet.**
- [ ] **Step 5: Commit as `test: define expanded daily edition acceptance criteria`.**

---

### Task 2: Write eight social-observation reports

**Files:**
- Create eight Markdown posts under `_posts/` dated `2026-08-01`.

**Interfaces:**
- Consumes: verified official releases and independent reporting for 2026-07-31.
- Produces: eight posts with `daily_section: social`, `importance: 101` through `108`, full source notes, SEO and WordPress metadata.

- [ ] **Step 1: Write disaster water, electricity and heat-risk report.**
- [ ] **Step 2: Write Kumamoto Red Cross emergency-care capacity report.**
- [ ] **Step 3: Write Kumamoto municipal cultural-facility closure report.**
- [ ] **Step 4: Write shared parenting and one-person caregiving burden report.**
- [ ] **Step 5: Write skilled-trades succession report.**
- [ ] **Step 6: Write accessible museum and co-viewing report.**
- [ ] **Step 7: Write Sixth Basic Environment Plan progress-review report.**
- [ ] **Step 8: Write Tokyo public-opinion survey report.**
- [ ] **Step 9: Run metadata validation and correct every missing body-tag match.**
- [ ] **Step 10: Commit as `content: add social observation reports for July 31`.**

---

### Task 3: Write ten science, culture, city and other reports

**Files:**
- Create ten Markdown posts under `_posts/` dated `2026-08-01`.

**Interfaces:**
- Consumes: official museum, conference, venue, sports and film sources.
- Produces: ten posts with `daily_section: other`, `importance: 201` through `210`, full source notes, SEO and WordPress metadata.

- [ ] **Step 1: Write National Museum of Nature and Science / RIHN exhibition report.**
- [ ] **Step 2: Write Conrad Nagoya opening and Sakae redevelopment report.**
- [ ] **Step 3: Write National Art Center family-program report.**
- [ ] **Step 4: Write Yoshimura Akira study memorial report.**
- [ ] **Step 5: Write Okayama wooden-vessel exhibition report.**
- [ ] **Step 6: Write Japan Society for Medical Education conference report.**
- [ ] **Step 7: Write medical-physics summer seminar report.**
- [ ] **Step 8: Write July 31 cinema-opening report.**
- [ ] **Step 9: Write NPB July 31 game roundup.**
- [ ] **Step 10: Write Kasai Rinkai Park sunflower-lighting report.**
- [ ] **Step 11: Run metadata validation and correct every missing body-tag match.**
- [ ] **Step 12: Commit as `content: add science culture city and sports reports`.**

---

### Task 4: Recompose the daily and homepage

**Files:**
- Modify: `daily/2026-07-31.md`
- Modify: `index.md`
- Modify: `assets/main.scss`

**Interfaces:**
- Consumes: `news_date`, `daily_section`, `importance`, article excerpts and tags.
- Produces: three separately rendered layers and homepage discovery sections.

- [ ] **Step 1: Query core, social and other posts independently and sort each by `importance`.**
- [ ] **Step 2: Render core as the existing numbered news list.**
- [ ] **Step 3: Render social as two-column article cards with excerpt and six tags.**
- [ ] **Step 4: Render other as compact cards with excerpt and four tags.**
- [ ] **Step 5: Update the daily introduction and editorial note to describe the expanded scope without production jargon.**
- [ ] **Step 6: Keep the homepage’s first eight core reports and append four social plus six other entries.**
- [ ] **Step 7: Add responsive styles while preserving the existing paper, ink and accent palette.**
- [ ] **Step 8: Run full acceptance tests and Jekyll build.**
- [ ] **Step 9: Commit as `feat: publish expanded July 31 daily edition`.**

---

### Task 5: Review, merge and production verification

**Files:**
- No additional production files unless review reveals a defect.

**Interfaces:**
- Consumes: completed feature branch and CI evidence.
- Produces: deployed expanded daily edition.

- [ ] **Step 1: Confirm the diff contains 18 new posts, eight metadata-only edits and the intended page/test/style changes.**
- [ ] **Step 2: Confirm all existing permalinks are unchanged.**
- [ ] **Step 3: Confirm CI passes section counts, tags, WordPress parity and rendered headings.**
- [ ] **Step 4: Merge with title `feat: expand July 31 daily edition to 26 reports`.**
- [ ] **Step 5: Verify HTTP 200 and expected section text on the homepage, daily page and representative new social and other articles.**
- [ ] **Step 6: Record commit, workflow run and public URL evidence in the merged pull request.**
