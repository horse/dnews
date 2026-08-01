# 日本語版

このディレクトリには、WordPress公開用の日本語オリジナル原稿を保存する。中国語版の翻訳ではなく、日本語の公的資料と信頼できる報道を改めて確認して日本語で執筆する。

```text
posts/                  独立記事
daily/                  当日の全記事へのリンクを含む朝刊ページ
edition-YYYY-MM-DD.yml  版次、集計時間、実数、順序、ファイル対応を管理するmanifest
```

新しい版次は次の条件を満たす。

- `news_date` と `edition_date` は朝刊の版次日；
- `editorial_origin: japanese-sources`；
- `translation_status: original`；
- `publication_target: wordpress`；
- core 6—8本、social 8—12本、other 10—15本；
- manifestの`expected_counts`は当期の実数を記録；
- 各記事12—25タグ、本文中に同じ表記が存在；
- coreは1000字相当、socialは750字相当、otherは550字相当以上；
- core/socialは原則2件以上、otherは1件以上のリンク付き参照資料；
- `wordpress.status: publish` を標準とする。

三分類とも調査、確認、編集に同じ労力をかける。政治・経済記事は決定、数字、制度と影響を中心にし、社会記事は具体的事実から公共サービスや生活条件を説明する。その他の記事は現場性、知識、文化的背景を加えてよいが、告知や広報の要約にしてはならない。

全記事を書いた後、`tools/build_edition.py` を実行してmanifestと日次総覧を生成し、`tools/validate_edition.py` で検証する。日次総覧は当日の全記事の見出し、要約、公開URLを直接含む。

公開は追加方式で行う。新しい日付は新規記事と新規朝刊として公開し、過去の版次を上書きしない。同じ日の再実行だけが同じslugの記事を更新する。