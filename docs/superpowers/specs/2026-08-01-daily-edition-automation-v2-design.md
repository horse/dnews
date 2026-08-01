# 每日双语新闻早报自动化 V2 设计

## 目标

每天日本时间06:00由一个定时任务完成26个日本新闻事件的发现、研究、中日双语独立写作、仓库验证、GitHub Pages发布、WordPress发布和完成通知。

## 关键决定

- 候选池只使用可信新闻媒体和权威机构发布，不使用X、搜索趋势或社交热度。
- 版次日为运行当天，覆盖前一天06:00至当天05:59:59 JST。
- 每期固定8 core、8 social、10 other，共26个事件和52篇语言稿。
- 内容先进入独立分支，全部验证通过后才合并main。
- manifest、两种日报和26个日语链接由脚本生成，减少手工错误。
- 验证按manifest动态选择版次，不再写死2026-07-31或仓库总篇数。
- WordPress只发布发生变化的版次，默认publish，按slug幂等更新。

## 组件

- `tools/edition.py`：版次模型、稿件收集、manifest生成、日报渲染、动态验证、变更日期解析。
- `tools/build_edition.py`：为一个版次生成manifest和两种日报，并立即验证。
- `tools/validate_edition.py`：验证一个或全部版次。
- `tools/publish_wordpress.py`：按版次选择稿件并发布。
- CI：在PR中验证双语文章、版次结构和Jekyll页面。
- Release：合并main后分别部署Pages和WordPress。

## 失败隔离

发现或写作不足、源数据不合格、测试失败时不合并main；发布端失败时保留已合并内容并明确报告失败端。slug和版次日期保证重跑幂等。
