# WordPress发布映射

Markdown是内容正本。WordPress发布器读取YAML front matter，将正文渲染为HTML，并通过`/wp-json/wp/v2/posts`发布。

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

发布器按发生变化的版次工作，不扫描并重发全部历史文章。每期发布当期实际数量的日语独立稿和1篇日语日报，不假定固定26篇。

默认状态是`publish`，按slug幂等创建或更新；多个同slug对象会使任务失败。新日期增加新文章，历史日期保留；只有同一天重跑时才更新同slug内容。

认证信息只使用环境变量：

- `WP_BASE_URL`
- `WP_USERNAME`
- `WP_APP_PASSWORD`

不得提交密码、Application Password、JWT或其他凭据。