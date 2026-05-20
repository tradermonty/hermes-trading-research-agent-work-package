# 実装ブリーフ: Hermes Trading Research Agent

## 目的

`claude-trading-skills` の多数のスキルを、Hermes Agent上で「迷わず使える」常駐型トレードリサーチアシスタントとして配布する。

ユーザーが個別スキル名を覚える必要がないように、以下をパッケージ化する。

- Hermes Profile Distribution
- `SOUL.md` による人格・方針・禁止事項
- `skill-bundles/*.yaml` によるプリセットワークフロー
- cronによる朝・引け後・週次・月次ルーチン
- `claude-trading-skills` との外部リンク/ベンダリング同期スクリプト
- 安全性・非シグナルサービス方針・データ鮮度表示

## MVPの完成イメージ

利用者は以下だけで開始できる。

```bash
hermes profile install github.com/tradermonty/hermes-trading-research-agent-work-package --name trading-research-assistant --alias -y
trading-research-assistant chat
```

その後、チャットまたはTelegram/Slack等で以下を呼ぶ。

```text
/pre-market-routine 今日の寄り付き前チェックをして
/after-close-review 今日の引け後レビューをして
/trade-journal NVDAのエントリー判断を記録して
```

## 設計判断

初期版は `claude-trading-skills` をコピーせず、`skills.external_dirs` で外部参照する。これにより、スキル本体のメンテナンスは既存repoをcanonicalに保ち、このrepoは「Hermes向けプロファイル・ワークフロー・自動化レイヤー」に集中する。

後続で `--mode vendor` を実装し、選択スキルをこのrepoの `skills/vendor/` にコピーできるようにする。

## 最重要ガードレール

このエージェントは売買判断の外注先ではない。以下を固定する。

- 自動発注しない。
- 直接的なBuy/Sell指示を出さない。
- 候補銘柄はwatchlist/research candidateとして扱う。
- thesis / invalidation / risk notes / next human action を必ず出す。
- データがないときは推測で埋めない。
