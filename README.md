# dnews

`dnews` 是一套以“发现重要事件—重新检索—重新报道”为核心的日本新闻日报仓库。

本仓库同时服务两种发布方式：

1. **GitHub Pages**：Jekyll 直接读取 Markdown，自动生成公开网站。
2. **WordPress**：每篇稿件的 front matter 已包含 slug、摘要、分类、标签、SEO 标题和 meta description，可由后续同步脚本映射到 WordPress REST API。

## 内容结构

```text
_posts/                  独立新闻稿
daily/                   每日日报索引页
docs/editorial-guide.md  编辑与再报道规范
wordpress/README.md      WordPress 字段映射说明
assets/main.scss         站点样式
.github/workflows/       GitHub Pages 自动部署
```

## 日期口径

日报以日本标准时间（JST）计算。`2026-07-31` 日报收录 2026 年 7 月 31 日 00:00—23:59 之间形成的主要新闻事实；正文于次日完成检索和核验后发布。

## 发布

推送到 `main` 分支后，GitHub Actions 会构建并部署 Pages。首次启用时，如仓库尚未设定 Pages 来源，请在：

`Settings → Pages → Build and deployment → Source`

选择 **GitHub Actions**。

预定站点地址：

<https://horse.github.io/dnews/>

## 本地预览

```bash
bundle install
bundle exec jekyll serve
```

浏览器打开 `http://127.0.0.1:4000/dnews/`。

## 编辑原则

- 先按“事件”聚类，不按转载文章数量计数。
- 入选后重新查找第一手资料和独立报道，不拼接摘要。
- 标题与导语只使用已经确认的新事实。
- 分析用于解释，不得压过新闻事实。
- 公开正文与后台编辑字段分离。
- 对尚未确认的市场行为、调查结论和司法状态作明确限定。
