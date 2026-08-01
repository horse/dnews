# dnews

`dnews` 是一套每天一次完成的日本双语新闻早报系统。流程固定为四步：获取新闻条目、聚类并决定选稿、逐篇重新研究和写作、分别增量发布中文与日语版本。

## 每日版次

- 启动时间：日本时间每天06:00；
- 版次日期：运行当天；
- 覆盖窗口：前一天06:00:00至当天05:59:59（JST）；
- 政治经济与重大事件：6—8篇；
- 社会观察：8—12篇；
- 科学、文化、城市、体育及其他：10—15篇；
- 总计通常24—35个事件，每个事件都有中文和日语独立稿。

## 新闻入口

候选只从以下入口获取：

- Yahoo!ニュース主要页面；
- Google News日本头条；
- NHK NEWS WEB；
- 朝日、读卖、每日、日经、产经；
- 共同社、时事通信、NHK。

Yahoo!ニュース和Google News用于发现；正式写作回到原媒体、官方资料和可信独立报道。X、搜索趋势、粉丝讨论、访问排行榜、广告和抽奖不进入候选池。

## 四步生产流程

1. 读取覆盖窗口内的标题、媒体、发布时间、页面位置和链接；
2. 按事件合并重复条目，以页面位置和独立媒体重复情况为主要信号，再结合公共影响、制度意义、新事实强度、后果持续性、可靠性和紧急性决定三个分类的实际篇数；
3. 对每个入选事件重新搜索、核验并分别写成完整中文新闻和日语原生新闻；
4. 自动生成两种日报和manifest，验证后将中文增加到GitHub Pages，将日语增加到shinkiji。

三类新闻投入相同的检索、核验和编辑努力，只根据题材采用不同写法。

## 内容结构

```text
_posts/                          中文独立新闻稿
daily/                           中文每日早报页
japanese/posts/                  日语原生独立新闻稿
japanese/daily/                  日语WordPress早报页
japanese/edition-YYYY-MM-DD.yml  每期manifest
tools/edition.py                 版次生成与验证库
tools/build_edition.py           生成manifest和两种日报
tools/validate_edition.py        验证一个或全部版次
tools/publish_wordpress.py       按版次幂等同步WordPress
docs/editorial-guide.md          选稿和写作规范
docs/daily-automation-runbook.md 单任务执行手册
```

## 生成与验证

完成当期全部中日稿件后：

```bash
python tools/build_edition.py \
  --edition-date 2026-08-02 \
  --coverage-start 2026-08-01T06:00:00+09:00 \
  --coverage-end 2026-08-02T05:59:59+09:00 \
  --published-at '2026-08-02 06:00:00 +0900' \
  --wordpress-status publish

python tools/validate_edition.py --edition-date 2026-08-02
python -m unittest tests/test_edition.py tests/test_publish_wordpress.py -v
bundle exec jekyll build
EDITION_DATE=2026-08-02 SKIP_BUILD=1 bash tests/test_tags.sh
```

新版本manifest使用schema version 3，记录当期三个分类的实际篇数。历史schema version 1和2继续按原有8/8/10验证。

## 发布端

- 中文版：合并到`main`后由GitHub Actions部署到GitHub Pages；
- 日语版：由WordPress工作流只发布发生变化的当期稿件和日报；
- 两端都是按日期增加，不覆盖历史版次；
- 同一天重跑时按slug更新，避免重复文章；
- WordPress最终状态默认`publish`；
- 凭据只存放于GitHub Actions Secret `shinkiji`。