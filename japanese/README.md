# 日本語版

このディレクトリには、WordPress公開用の日本語オリジナル原稿を保存する。中国語版の翻訳ではなく、日本語の公的資料と信頼できる報道を改めて確認して日本語で執筆する。

```text
posts/                  独立記事
daily/                  26本へのリンクを含む朝刊ページ
edition-YYYY-MM-DD.yml  版次、集計時間、件数、順序、ファイル対応を管理するmanifest
```

新しい版次は次の条件を満たす。

- `news_date` と `edition_date` は朝刊の版次日；
- `editorial_origin: japanese-sources`；
- `translation_status: original`；
- `publication_target: wordpress`；
- 8本のcore、8本のsocial、10本のother；
- 各記事12—25タグ、本文中に同じ表記が存在；
- coreは1000字相当、socialは750字相当、otherは550字相当以上；
- core/socialは原則2件以上、otherは1件以上のリンク付き参照資料；
- `wordpress.status: publish` を標準とする。

26本を書いた後、`tools/build_edition.py` を実行してmanifestと日次総覧を生成し、`tools/validate_edition.py` で検証する。日次総覧は26本すべての見出し、要約、公開URLを直接含む。
