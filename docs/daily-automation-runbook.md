# 每日 06:00 单任务执行手册

## 固定参数

运行于日本时间每天 06:00。

```text
edition_date   = 当天 YYYY-MM-DD
coverage_start = 前一天 06:00:00+09:00
coverage_end   = 当天 05:59:59+09:00
branch         = news/<edition_date>-morning
```

## 执行步骤

1. 从 `main` 创建当天分支；若同名分支已存在，先检查是否为上次失败的未合并分支，继续修复而不是新建重复分支。
2. 检索过去24小时内可信新闻媒体和权威机构发布，建立60—120条候选。
3. 按事件去重，完成硬新闻与公共新闻兜底搜索。
4. 锁定26个事件：8 core、8 social、10 other。
5. 为每个事件建立资料包，核对新事实、时间、数字、主体、来源、未确认点和下一节点。
6. 写26篇中文稿到 `_posts/<edition_date>-<slug>.md`。
7. 用相同slug写26篇日语原生稿到 `japanese/posts/<edition_date>-<slug>.md`。
8. 两种语言的新稿都使用 `news_date` 和 `edition_date` 为当天版次日期；日语稿的 `wordpress.status` 写 `publish`。
9. 执行：

```bash
python tools/build_edition.py \
  --edition-date "$edition_date" \
  --coverage-start "$coverage_start" \
  --coverage-end "$coverage_end" \
  --published-at "$edition_date 06:00:00 +0900" \
  --wordpress-status publish
```

10. 执行完整验证：

```bash
python -m unittest tests/test_edition.py tests/test_publish_wordpress.py -v
python tools/validate_edition.py --edition-date "$edition_date"
bundle exec jekyll build
EDITION_DATE="$edition_date" SKIP_BUILD=1 bash tests/test_tags.sh
```

11. 提交分支、创建PR，等待全部CI完成。任何检查失败都在分支修复，不得把不完整内容推入 `main`。
12. CI全绿后合并PR。
13. 等待 Pages 与 WordPress 工作流完成；WordPress工作流应只处理当前版次27篇内容（26篇独立稿＋1篇日报）。
14. 检查中文版日报、日语日报及27个日语URL。只有公开验证成功后才通知用户。

## 失败规则

- 候选不足26个可靠事件：失败，不凑数；
- 任一语言少于26篇：失败；
- 8/8/10不符：失败；
- 日中slug不一致：失败；
- 来源、篇幅、标签或元数据不合格：失败；
- CI失败：不合并；
- WordPress或Pages失败：明确报告发布端失败，不声称已完成；
- 重跑时复用同一slug和同一分支，避免重复文章。

## 完成通知

通知只包括：

- 版次日期与覆盖窗口；
- 8/8/10共26篇；
- 中文日报URL；
- 日语日报URL；
- Pages和WordPress验证结果；
- 有无需要特别注意的事实修正。
