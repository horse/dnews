# WordPress 发布映射

Markdown 是内容正本。WordPress 发布器读取 YAML front matter，将正文渲染为 HTML，并通过 `/wp-json/wp/v2/posts` 发布。

| Markdown | WordPress |
|---|---|
| `title` | `title` |
| Markdown正文 | HTML `content` |
| `excerpt` | `excerpt` |
| `slug` | `slug` |
| `date` | `date` |
| `wordpress.status`或工作流状态 | `status` |
| `wordpress.categories` | 查询/创建后传分类ID |
| `wordpress.tags` | 查询/创建后传标签ID |

发布器按版次工作，不再扫描并重发全部历史文章。默认状态是 `publish`，按slug幂等创建或更新；多个同slug对象会使任务失败。

认证信息只使用环境变量：

- `WP_BASE_URL`
- `WP_USERNAME`
- `WP_APP_PASSWORD`

不得提交密码、Application Password、JWT或其他凭据。
