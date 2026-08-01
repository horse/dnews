# Simplified Daily News Pipeline Design

## Goal

Make the daily bilingual edition run from one clear four-step process: collect a fixed set of Japanese news feeds, rank clustered events, write every selected item as a full news article in both languages, and append-publish Japanese to shinkiji and Chinese to GitHub Pages.

## Coverage window

Every run uses Japan Standard Time:

- start: previous day 06:00:00
- end: current day 05:59:59
- edition date: current day

## Candidate sources

Discovery is limited to:

- Yahoo!ニュース main pages
- Google News Japan top stories
- NHK NEWS WEB
- 朝日新聞
- 読売新聞
- 毎日新聞
- 日本経済新聞
- 産経新聞
- 共同通信
- 時事通信
- NHK

Discovery records headline, publisher, publication time, page position and URL. Yahoo!ニュース and Google News are discovery indexes; reporting returns to the original publisher, official documents and reliable independent coverage.

## Selection

Articles covering the same event are clustered. Page prominence and independent repetition are the primary signals. Editorial scoring then considers public impact, institutional significance, strength of the new fact, duration of consequences, source reliability, independent confirmation and urgency.

Section ranges:

- core: 6–8
- social: 8–12
- other: 10–15
- total: normally 24–35

The manifest records the actual count for each section. The system must not fill to the upper bound with weak items.

## Writing

Every selected event receives the same research, verification and editing effort. Core stories emphasize decisions, figures, institutions and consequences. Social stories explain public services and lived conditions from a concrete new fact. Other stories may use more scene, knowledge or cultural context, but remain full reported news rather than notices or publicity.

Chinese and Japanese share the event, facts, slug, section and order. Japanese is independently written from Japanese sources, not translated from Chinese.

## Publishing

Chinese files append to `_posts/` and `daily/`, then publish through GitHub Pages. Japanese files append to `japanese/posts/` and `japanese/daily/`, then publish to shinkiji through the existing WordPress workflow. Historical editions are never replaced. A rerun only updates matching slugs for the same edition.

## Compatibility

Existing schema version 1 and 2 editions remain valid with their fixed 8/8/10 counts. New flexible editions use schema version 3 and validate actual counts against the ranges above.