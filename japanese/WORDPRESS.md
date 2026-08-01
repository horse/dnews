# WordPress下書き契約

日本語記事は `japanese/posts/*.md` を正本とする。後続の同期ツールはfront matterを読み、Markdown本文をHTMLへ変換してWordPress REST APIへ送る。

## 必須動作

1. `slug` で既存記事を検索する。
2. 該当記事がなければ `draft` を新規作成する。
3. 1件あれば同じ投稿を更新する。
4. 複数件あれば処理を停止する。
5. カテゴリーとタグは名前で検索し、存在しなければ作成する。
6. `wordpress.status`、`wordpress.post_type`、`wordpress.comment_status` を送信する。
7. 認証情報はGitHub Actions Secretsから読み、リポジトリへ保存しない。

## 認証

WordPressの専用投稿ユーザーとApplication Passwordを使う。必要な環境変数は次の3つ。

- `WP_BASE_URL`
- `WP_USERNAME`
- `WP_APP_PASSWORD`

初期運用では全投稿を下書きとして同期し、WordPress上で確認してから公開する。
