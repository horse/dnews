# dnews 日本語オリジナル版設計

## 目的

既存の簡体字中国語版26本を変更せず、日本語の一次資料と日本語報道を直接確認して執筆した日本語版26本を同一リポジトリに追加する。日本語版はWordPressの下書き原稿として管理し、中国語版は従来どおりGitHub Pagesで公開する。

## 編集上の原則

- 日本語版は中国語版の翻訳ではない。
- 両言語は同じ出来事を扱い、`story_id` と `slug` で対応させる。
- 日付、数値、人名、組織、発表・検討・決定・実施の段階は一致させる。
- 見出し、導入、段落構成、説明量、カテゴリー、タグは各言語の読者に合わせて独立して設計する。
- 日本語版も `core 8 / social 8 / other 10` の三層を維持する。

## 保存場所

- `japanese/posts/`: WordPress用の独立記事26本
- `japanese/daily/`: 日次総覧
- `japanese/edition-2026-07-31.yml`: 記事一覧と順序を管理するマニフェスト

`japanese/` はJekyllの `exclude` に追加し、中国語GitHub Pagesには出力しない。

## WordPressフィールド

各記事は `publication_target: wordpress`、`wordpress.status: draft`、`wordpress.post_type: post`、`wordpress.comment_status: closed` を持つ。トップレベルのカテゴリー・タグとWordPress用のカテゴリー・タグを一致させ、後続のREST API同期に使用する。

## 検証

- 記事数は26本、内訳は8・8・10。
- 全記事に必須front matterを要求する。
- タグは12〜25個とし、すべて本文に逐語的に現れる。
- 日本語版と中国語版のslug集合を一致させる。
- 日次総覧に26本すべての見出しを含める。
- 中国語GitHub PagesのJekyllビルドを成功させ、日本語ディレクトリが公開成果物に含まれないことを確認する。
