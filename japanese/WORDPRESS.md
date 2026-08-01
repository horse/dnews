# WordPress公開契約

日本語記事は `japanese/posts/*.md` を正本とする。同期ツールはfront matterを読み、Markdown本文をHTMLへ変換してWordPress REST APIへ送る。

## 標準動作

1. `slug` で既存記事を検索する。
2. 該当記事がなければ、API上で投稿を作成する。
3. 標準の最終状態は `publish` とする。
4. 1件あれば同じ投稿を更新し、重複投稿を作らない。
5. 複数件あれば処理を停止する。
6. カテゴリーとタグは名前で検索し、存在しなければ作成する。
7. 認証情報はGitHub Actions Secretsから読み、リポジトリへ保存しない。

手動実行時に `draft` を明示した場合だけ、最終状態を下書きにする。

## 認証

WordPressの専用投稿ユーザーとApplication Passwordを使う。必要な環境変数は次の3つ。

- `WP_BASE_URL`
- `WP_USERNAME`
- `WP_APP_PASSWORD`

現在の正式ワークフローでは、サイトURLとユーザー名をコード側に設定し、Application PasswordだけをGitHub Actions Secret `shinkiji` から読み込む。
