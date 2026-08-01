# Tag Navigation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Display meaningful article tags across the dnews site, provide a tag index, and ensure tag metadata is complete and grounded in article text.

**Architecture:** Keep article front matter as the single source of truth. A reusable Liquid include renders tag pills in the post layout, homepage and daily edition; a static Jekyll tag index reads `site.tags`. A shell acceptance test builds with the GitHub Pages environment and validates rendered pages plus front matter quality.

**Tech Stack:** Jekyll 3.10, Liquid, Minima 2.5, SCSS, Bash, Ruby YAML, GitHub Actions.

## Global Constraints

- Each article must contain 12–25 tags.
- Every tag must occur verbatim in that article body.
- Tags cover names, places, organizations, institutions, formal events, industries and useful topic nouns.
- Categories remain broad sections; tags remain specific entities and concepts.
- The same front matter tags must feed GitHub Pages and WordPress.
- Existing public URLs must not change.

---

### Task 1: Add the failing tag acceptance test

**Files:**
- Create: `tests/test_tags.sh`
- Create: `.github/workflows/tags-ci.yml`

**Interfaces:**
- Consumes: Jekyll source files and article front matter.
- Produces: a CI check that validates rendered tag UI and tag data quality.

- [ ] **Step 1: Write the failing test**

Create `tests/test_tags.sh` to assert that `_site/tags/index.html` exists; tag pills appear on the homepage, daily page and article page; the tag index links back to an article; and every post has 12–25 tags that appear verbatim in its body.

- [ ] **Step 2: Run the test to verify it fails**

Run through a pull-request workflow using `actions/jekyll-build-pages@v1`, then execute `SKIP_BUILD=1 bash tests/test_tags.sh`.

Expected: FAIL because `/tags/`, tag-pill markup and expanded article tags do not yet exist.

- [ ] **Step 3: Commit the red test**

Commit message: `test: define tag navigation acceptance criteria`.

---

### Task 2: Add reusable tag rendering and navigation

**Files:**
- Create: `_includes/tag-list.html`
- Create: `_layouts/post.html`
- Create: `tags.md`
- Modify: `_config.yml`
- Modify: `assets/main.scss`

**Interfaces:**
- Consumes: `page.tags`, `post.tags`, `site.tags`.
- Produces: tag pill HTML, article metadata display and `/tags/` browsing page.

- [ ] **Step 1: Implement the tag-list include**

Render linked `.tag-pill` elements. Support `limit`, `compact` and `label` include parameters. Link every pill to the matching Unicode anchor on `/tags/`.

- [ ] **Step 2: Add the custom post layout**

Preserve Minima article semantics and existing URLs. Show news date and categories under the title, and show all tags after the article body under “相关标签”.

- [ ] **Step 3: Add the tag index**

Iterate over sorted `site.tags`, show article counts and links to all matching articles. Give each tag heading an anchor using the raw escaped tag name.

- [ ] **Step 4: Add navigation and styles**

Add `tags.md` to `header_pages`. Style tag pills, tag groups and article tag metadata without changing the existing palette.

- [ ] **Step 5: Run the acceptance test**

Expected: rendered-UI checks pass; metadata checks still fail until Task 3 expands the post tags.

---

### Task 3: Expand tags and reuse them on listing pages

**Files:**
- Modify: `index.md`
- Modify: `daily/2026-07-31.md`
- Modify: all eight files under `_posts/`

**Interfaces:**
- Consumes: tag include from Task 2 and each article's front matter.
- Produces: consistent tag displays and grounded 12–25-item tag sets.

- [ ] **Step 1: Update the homepage**

Include the first six tags under each news-card excerpt and link overflow to `/tags/`.

- [ ] **Step 2: Make the daily article list data-driven**

Replace the duplicated hard-coded `<ol>` with a Liquid query selecting posts whose `news_date` equals the page `news_date`, sorted by `importance`. Render title, excerpt and the first six tags.

- [ ] **Step 3: Expand the eight tag sets**

For every post, select 12–25 exact strings found in the article body. Mirror the same list under `wordpress.tags`.

- [ ] **Step 4: Run the full acceptance test**

Expected: PASS with all rendered checks and all metadata checks green.

---

### Task 4: Review, merge and verify production

**Files:**
- No new production files.

**Interfaces:**
- Consumes: completed feature branch.
- Produces: deployed GitHub Pages site with public tag navigation.

- [ ] **Step 1: Review the branch diff**

Confirm only tag-related layouts, styles, metadata, tests and documentation changed. Confirm no article URL or body fact was altered.

- [ ] **Step 2: Merge the pull request**

Use squash merge with commit title `feat: add article tag navigation`.

- [ ] **Step 3: Verify Pages deployment**

Probe the homepage, `/tags/`, the daily page and the Kumamoto article. Require HTTP 200 and expected tag text on each page.

- [ ] **Step 4: Record verification evidence**

Add a concise PR comment with the workflow run ID, successful build result and public URLs checked.
