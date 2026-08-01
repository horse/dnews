# WordPress公開契約

日本語記事の正本は `japanese/posts/*.md`、日次総覧の正本は `japanese/daily/*.md` とする。

## 標準動作

1. 版次manifestから対象日を特定する。
2. その版次の26記事と日次総覧1件だけを選ぶ。
3. MarkdownをHTMLへ変換する。
4. カテゴリーとタグを名前で再利用し、存在しない場合だけ作成する。
5. slugで既存投稿を検索する。
6. 0件なら作成、1件なら更新、複数件なら停止する。
7. 最終状態は標準で `publish`。手動実行時だけ `draft` を選択できる。
8. 公開後に全URLを未ログイン状態で確認する。

## 自動実行

`.github/workflows/publish-japanese-wordpress.yml` は `main` に入った変更から版次日を抽出し、その版次だけを同期する。過去の全記事を毎回再送しない。

## 認証

```text
WP_BASE_URL=https://shinkiji.com
WP_USERNAME=shinkiji
WP_APP_PASSWORD=${{ secrets.shinkiji }}
```

Application PasswordはGitHub Actions Secretにのみ保存し、リポジトリ、レポート、ログへ書き込まない。
