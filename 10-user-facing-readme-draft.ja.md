# Hermes Trading Research Assistant 日本語README下書き

このリポジトリは、Hermes Agent上で動くトレード用リサーチアシスタントのプロファイル配布パッケージです。

`claude-trading-skills` のスキル群を、寄り付き前チェック、引け後レビュー、決算銘柄チェック、トレード記録、週次ポートフォリオレビューなどのプリセットとして使えるようにします。

## これは何ではないか

- 売買シグナル配信サービスではありません。
- 自動売買システムではありません。
- 投資助言サービスではありません。
- 利益を保証するものではありません。

## できること

- 朝の相場環境チェック
- 決算で大きく動いている銘柄の確認
- 市場のリスクオン/リスクオフ判断材料の整理
- スイング候補の調査キュー作成
- トレード記録の構造化
- 引け後レビュー
- 週次・月次の振り返り

## インストール例

```bash
hermes profile install github.com/tradermonty/hermes-trading-research-agent --alias
trading-research-assistant chat
```

## 使い方例

```text
/pre-market-routine 今日の寄り付き前チェックをして
/after-close-review 今日の引け後レビューをして
/earnings-movers-triage 決算で大きく動いている銘柄を見て
/trade-journal 今日のNVDAの判断を記録して
```

## APIキー

一部のスキルはFMP、FINVIZ Elite、Alpaca paper/read-onlyなどのAPIキーを使うと機能が拡張されます。APIキーがない場合は、可能な範囲でdegraded modeとして動作します。
