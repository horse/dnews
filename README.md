# dnews

`dnews` 是一套每天一次完成的日本双语新闻早报系统：从可信新闻媒体与权威机构发布中发现事件，按事件去重，重新检索资料，分别写成中文与日语原生新闻，再发布到 GitHub Pages 和 WordPress。

## 每日版次

- 固定启动：日本时间每天 06:00。
- 版次日期：运行当天，例如 `2026-08-02`。
- 覆盖窗口：前一天 06:00:00 至当天 05:59:59（JST）。
- 新闻量：26 个事件，每个事件都有中文和日语独立稿。
- 结构：8 篇 `core`、8 篇 `social`、10 篇 `other`。
- 候选池只来自新闻媒体和正式发布；X、搜索趋势、访问排行和社交热度不进入候选池。

## 内容结构

```text
_posts/                         中文独立新闻稿
daily/                          中文每日早报页
japanese/posts/                 日语原生独立新闻稿
japanese/daily/                 日语 WordPress 早报页
japanese/edition-YYYY-MM-DD.yml 每期 manifest
tools/edition.py                版次发现、生成与验证库
tools/build_edition.py          生成 manifest 和两种日报
tools/validate_edition.py       动态验证一个或全部版次
tools/publish_wordpress.py      按版次幂等同步 WordPress
docs/editorial-guide.md         新闻发现、筛选和写作规范
docs/daily-automation-runbook.md 单任务执行手册
```

## 每期生产顺序

1. 建立 60—120 条真实新闻候选；
2. 按事件聚类，去除通讯社重复转载；
3. 选定 8/8/10 共 26 个事件；
4. 为每个事件重新检索日语官方资料和可信独立报道；
5. 分别写 26 篇中文稿和 26 篇日语原生稿；
6. 运行 `tools/build_edition.py` 自动生成 manifest、中文日报和日文日报；
7. 运行动态验证和 Jekyll 构建；
8. 在独立分支提交，CI 全部通过后才合并 `main`；
9. `main` 触发 GitHub Pages 和当期 WordPress 发布；
10. 验证公开 URL 后报告完成。

## 本地生成与验证

```bash
python -m pip install PyYAML Markdown requests

python tools/build_edition.py \
  --edition-date 2026-08-02 \
  --coverage-start 2026-08-01T06:00:00+09:00 \
  --coverage-end 2026-08-02T05:59:59+09:00 \
  --published-at '2026-08-02 06:00:00 +0900' \
  --wordpress-status publish

python tools/validate_edition.py --edition-date 2026-08-02
python -m unittest tests/test_edition.py tests/test_publish_wordpress.py -v
bundle exec jekyll build
SKIP_BUILD=1 bash tests/test_tags.sh
```

## 发布端

- 中文版：合并到 `main` 后由 `.github/workflows/pages.yml` 部署到 GitHub Pages。
- 日文版：日语稿、日语日报或 manifest 进入 `main` 后，由 `.github/workflows/publish-japanese-wordpress.yml` 只发布发生变化的版次。
- WordPress 最终状态默认是 `publish`；手动运行时可以明确改为 `draft`。
- WordPress 通过 slug 创建或更新，避免重复文章。
- 凭据只存放于 GitHub Actions Secret `shinkiji`。
