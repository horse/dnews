# 每日06:00单任务执行手册

## 固定参数

```text
edition_date   = 日本时间运行当天 YYYY-MM-DD
coverage_start = 前一天 06:00:00+09:00
coverage_end   = 当天 05:59:59+09:00
branch         = news/<edition_date>-morning
```

历史内容只增加，不覆盖。当天任务重跑时复用同一分支和同一slug。

## 第一步：获取新闻信息

只读取覆盖窗口内的以下新闻入口：

- Yahoo!ニュース主要页面
- Google News日本头条
- NHK NEWS WEB
- 朝日新闻
- 读卖新闻
- 每日新闻
- 日本经济新闻
- 产经新闻
- 共同社
- 时事通信
- NHK

每条候选至少记录：标题、媒体、发布时间、所在页面及位置、链接。Yahoo!ニュース和Google News用于新闻发现；进入写作后必须返回原媒体、官方资料和可信独立报道核验。

不使用X、Google Trends、搜索热词、粉丝讨论、访问排行榜、广告或抽奖。

## 第二步：聚类、判断与确定篇数

先按事件合并重复条目：

- 同一通讯社稿的转载只算一个信号；
- 同一事件的多次更新合并，保留最新事实；
- 只有主体、影响对象或新闻问题明显不同，才可拆成多篇。

主要判断信号：

1. 新闻在Yahoo!ニュース、Google News、NHK及各媒体页面中的位置；
2. 有多少家独立媒体重复报道同一事件；
3. 是否持续更新。

再结合：公共影响、制度意义、新事实强度、后果持续性、来源可靠性、独立确认和紧急性。

最终篇数按当天新闻量决定：

- 政治经济与重大事件：6—8篇；
- 社会观察：8—12篇；
- 科学、文化、城市、体育及其他：10—15篇；
- 总计通常24—35篇。

不得为了达到上限凑数。重大灾害、重大政策决定、关键经济数据、国家安全和重大司法结果强制优先。

## 第三步：逐篇研究、写作与存档

每条入选新闻都重新搜索和建立资料包，至少核对：

- 当天的新事实和准确时间；
- 人物、机构和数字口径；
- 原报道和第一手正式资料；
- 必要的独立报道；
- 尚未确认的部分；
- 下一次会议、实施、公布、审理或恢复节点。

三类新闻投入相同的检索、核验和编辑努力：

- 政治经济稿强调决定、数字、制度和后果；
- 社会观察稿从当天事实解释公共服务、劳动、家庭、医疗、教育和地方生活；
- 其他稿可增加现场感、知识性或文化背景，但仍须是完整新闻，不得写成预告、宣传稿或简单摘要。

中文稿写入：

```text
_posts/<edition_date>-<slug>.md
```

日语稿依据日语资料独立写作，写入：

```text
japanese/posts/<edition_date>-<slug>.md
```

日语不是中文翻译。两种语言共享事件、事实、slug、分类和排序。

## 第四步：生成、验证与增量发布

完成全部双语独立稿后运行：

```bash
python tools/build_edition.py \
  --edition-date "$edition_date" \
  --coverage-start "$coverage_start" \
  --coverage-end "$coverage_end" \
  --published-at "$edition_date 06:00:00 +0900" \
  --wordpress-status publish
```

生成器根据实际稿件数量自动建立：

- `daily/<edition_date>.md`；
- `japanese/daily/<edition_date>.md`；
- `japanese/edition-<edition_date>.yml`。

manifest记录当期三个分类的实际篇数。新版本验证范围为6—8、8—12、10—15；旧版次继续按其原有固定数量验证。

完整验证：

```bash
python -m unittest tests/test_edition.py tests/test_publish_wordpress.py -v
python tools/validate_edition.py --edition-date "$edition_date"
bundle exec jekyll build
EDITION_DATE="$edition_date" SKIP_BUILD=1 bash tests/test_tags.sh
```

全部通过后才提交当天分支、创建PR并等待CI。CI全绿后合并main：

- 中文版增加到GitHub Pages；
- 日语版按本次版次发布到shinkiji；
- WordPress按slug创建或更新，不重复创建；
- 旧日期的文章和日报不得删除或覆盖。

## 失败规则

- 任一分类低于下限或超过上限：停止；
- 中日篇数、slug或分类不一致：停止；
- 来源、事实、篇幅、标签或元数据不合格：停止；
- CI、Pages或WordPress失败：明确报告失败阶段，不声称已经发布；
- 不得通过缩短日语稿、降低核验或加入弱新闻来掩盖失败。

## 完成通知

只报告：版次日期、覆盖窗口、三个分类的实际篇数、总篇数、中文日报URL、日语日报URL、Pages与WordPress验证结果及重要事实修正。