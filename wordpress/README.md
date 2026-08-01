# WordPress 发布映射

仓库中的 Markdown 是内容底稿。GitHub Pages 直接读取；WordPress 发布器则应读取 front matter，将字段映射到 `/wp-json/wp/v2/posts`。

## 标准字段

| Markdown front matter | WordPress |
|---|---|
| `title` | `title` |
| 正文 Markdown 渲染后的 HTML | `content` |
| `excerpt` | `excerpt` |
| `slug` | `slug` |
| `date` | `date` |
| `wordpress.status` | `status` |
| `wordpress.categories` | 先按名称或 slug 查询/创建，再传 ID |
| `wordpress.tags` | 先按名称或 slug 查询/创建，再传 ID |

## 扩展字段

建议在 WordPress 中用 `register_post_meta` 注册以下字段：

- `news_date`
- `article_type`
- `analysis_angle`
- `importance`
- `source_checked_at`

`seo_title` 和 `meta_description` 需要按照实际采用的 SEO 插件映射。Yoast SEO、Rank Math、SEOPress 的字段并不相同，不应把插件专用键写死在内容文件里。

## 发布流程

1. 读取 `_posts/*.md`。
2. 解析 YAML front matter 和 Markdown 正文。
3. 按 slug 查询现有文章，避免重复发布。
4. 解析并同步分类、标签。
5. 将 Markdown 转为 HTML。
6. 以 `draft` 创建或更新 WordPress 文章。
7. 编辑确认后改为 `publish`。
8. 将 WordPress post ID 和最终 URL 写入独立的同步清单，而不要回写新闻正文。

不得在仓库提交 WordPress 密码、Application Password、JWT 或其他凭据。GitHub Actions 使用时应存入 repository secrets。
