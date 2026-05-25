# Hermes Trading Research Agent (日本語版)

Hermes Agent上で動作する、米国株個人投資家向けのリサーチ・プロセス支援アシスタントです。`tradermonty/claude-trading-skills` のスキル群を、寄り付き前チェック / 引け後レビュー / 決算銘柄トリアージ / トレード記録などのプリセット (スラッシュコマンド) として呼び出せるようにします。

**ランディングページ:** https://tradermonty.github.io/hermes-trading-research-agent-work-package/

**これは自動売買システムではありません。** リサーチ・記録・リスクレビューの支援ツールであり、最終的な売買判断は常に人間 (利用者) が行います。注文発注も、シグナル配信も、隠しジョブもありません。

- Hermes alias: `trading-research-assistant`
- 動作確認済み Hermes バージョン: **v0.14.0** (2026.5.16)
- デフォルトスケジュール timezone: `America/Los_Angeles` ([タイムゾーンの扱い](#タイムゾーンの扱い重要) 参照)

---

## クイックスタート (5分)

### 最短手順: Hermesに導入を依頼する

Hermesにセットアップ用のターミナル操作を任せてよい場合は、まずHermes Agentをインストールしてから、Hermes本人にこのprofileの導入を依頼できます。

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
hermes setup
hermes
```

Hermesチャットに以下を貼り付けてください:

```text
以下のHermes Trading Research Agent profileを導入してください。
https://github.com/tradermonty/hermes-trading-research-agent-work-package

上流スキルリポジトリはこちらです。
https://github.com/tradermonty/claude-trading-skills

aliasは trading-research-assistant にしてください。
ブローカー連携はpaper/read-only前提のままにしてください。
導入後、/pre-market-routine の実行方法も教えてください。
```

### 手動手順

```bash
# 1. このリポジトリと上流のスキルリポジトリを clone
git clone <this-repo-url> hermes-trading-research-agent
git clone https://github.com/tradermonty/claude-trading-skills.git
cd hermes-trading-research-agent

# 2. 上流スキルの場所を指定
export CLAUDE_TRADING_SKILLS_REPO="$(realpath ../claude-trading-skills)"

# 3. スケルトン検証
make validate
make test    # 87 tests pass

# 4. 全 skill 参照が上流に存在するか確認
python3 scripts/validate_upstream_index.py \
  --source "$CLAUDE_TRADING_SKILLS_REPO" --profile-root .

# 5. profile install (or GitHub から直接)
hermes profile install "$(pwd)" --name trading-research-assistant --alias -y
# あるいは:
#   hermes profile install github.com/tradermonty/hermes-trading-research-agent-work-package \
#     --name trading-research-assistant --alias -y

# model/provider 設定 (Hermes setup に合わせる)
trading-research-assistant config set model    claude-opus-4-7
trading-research-assistant config set provider anthropic
# 他 provider 例:
#   trading-research-assistant config set provider     openai-codex
#   trading-research-assistant config set model        gpt-5.5
#   trading-research-assistant config set model.base_url https://chatgpt.com/backend-api/codex
# (dotted key `model.default` / `model.provider` でも動作)

# 6. APIキーを設定
cp ~/.hermes/profiles/trading-research-assistant/.env.EXAMPLE \
   ~/.hermes/profiles/trading-research-assistant/.env
# .env をエディタで開き、必要なキーを記入

# 6b. 一部 skill / script が直接 import する Python deps をインストール
#     - trader-memory-core (上流) は jsonschema を import
#     - cron/create_cron_jobs.py は schedule preset 読み込みで pyyaml を import
python3 -m pip install jsonschema pyyaml
# (または: uv pip install jsonschema pyyaml)

# 7. 起動
trading-research-assistant chat
# チャットセッション内で:
#   /pre-market-routine
#   /after-close-review
#   /trade-journal
```

---

## 前提条件

| 必要なもの | 備考 |
|---|---|
| Hermes Agent CLI v0.12.0以上 (v0.14.0 で動作確認済み) | https://hermes-agent.nousresearch.com/ |
| Python 3.11 以上 | 検証スクリプト・テスト用 |
| `tradermonty/claude-trading-skills` を local に clone | external-linked mode で `CLAUDE_TRADING_SKILLS_REPO` から参照 |

### APIキー

全てのキーは install 時点では **任意** です (`distribution.yaml` で `required: false`)。キーが無い場合、該当する skill は **degraded mode** で動作し、出力にその旨が記載されます。

- **推奨** (無いと一部 skill が degraded mode に):
  - `FMP_API_KEY` — Financial Modeling Prep。決算・経済指標・財務・OHLCV を扱うスキルで使用。
  - `FINVIZ_API_KEY` — FINVIZ Elite。スクリーナー系スキルで使用。
- **いずれか1つ必要** (chat / cron の LLM 呼び出し用):
  - `ANTHROPIC_API_KEY` / `OPENAI_API_KEY` / `OPENROUTER_API_KEY` (`config set provider` で指定した値と一致させる)。
- **任意**:
  - `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` — デフォルトで paper / read-only (`ALPACA_PAPER=true`)。

---

## スラッシュコマンド (10個)

| スラッシュコマンド | デフォルト cron | 用途 |
|---|---|---|
| `/pre-market-routine` | 平日 06:00 PT | マクロカレンダー、相場環境、決算銘柄、ブレッド、ウォッチリスト候補、リスクゲート |
| `/after-close-review` | 平日 13:15 PT | 今日の変化、セクターローテ、保有銘柄レビュー、ジャーナル素材、明日の準備 |
| `/market-regime-daily` | 手動 / 随時 | 15分の相場環境チェック (ブレッド、上昇銘柄比率、エクスポージャー上限) |
| `/swing-opportunity-daily` | リスクゲート許可時のみ手動 | 規律あるスイング候補発掘 (仮説 / 否定条件 / ポジションサイズ前提) |
| `/earnings-movers-triage` | イベント駆動 | 決算ギャップ銘柄と PEAD 候補の分類 |
| `/portfolio-risk-check` | 手動 | エクスポージャー、集中度、ポートフォリオヒート、保有仮説の有効性 |
| `/trade-journal` | 手動 | トレードメモを仮説 / 否定条件 / リスク記録付きの構造化ジャーナルへ |
| `/trade-ticket` | 手動 | 候補を JSON-Schema 検証付きの trade ticket として記録、明示的な human approval gate (`DRAFT` / `REVIEW_READY` / `APPROVED` / `REJECTED` / `EXPIRED`) を伴う。ticket 出力のみで **発注は一切しない**。保存は operator-confirmed (`HERMES_TRADE_TICKET_DIR`、推奨 basename `<ticket_id>.ticket.yaml`)、optional な `journal_bridge` block で APPROVED ticket を `trader-memory-core` に handoff。`schemas/trade-ticket.schema.json` と `docs/04-skill-integration-strategy.md` の "Trade ticket primitive" / "Ticket persistence and journal bridge" 節を参照 |
| `/weekly-portfolio-review` | 土曜 09:00 PT | 長期保有・配当・アロケーションドリフト・要レビュー銘柄 |
| `/monthly-performance-review` | 月初 09:00 PT | プロセスレビュー、シグナル postmortem、来月の運用ルール |

すべての bundle の instruction は **データ鮮度 / 出典 (どの skill / data source か) / 仮説 / 否定条件 / リスク考察 / 人間の最終判断ゲート** を出力に含めることを強制します (`tests/test_required_sections.py`)。

---

## cron ジョブの有効化

```bash
export HERMES_PROFILE_CMD=trading-research-assistant
export HERMES_CRON_DELIVER=local   # または telegram / discord / slack / origin
bash cron/create_cron_jobs.sh
trading-research-assistant cron list
```

`data/schedule-presets.yaml` が4つの cron job の **単一の source of truth** です (schedule + name + skills + prompt file + 期待 timezone)。シェルスクリプトは `cron/create_cron_jobs.py` の thin wrapper で、YAML を読んで preset 順に `cron create` を発行し、host の IANA timezone が preset と異なる場合は **stderr に WARNING** を出力します (IANA 名比較のため、UTC offset が一致しても `America/Phoenix` vs `America/Los_Angeles` のような mismatch は検出されます)。`cron/create_cron_jobs.py --dry-run` で実行せずに発行コマンドを確認可能。

スケジュール対象 prompt には `{{TIMEZONE}}` テンプレートが含まれていて、cron-create 時に runtime が展開します。優先度は **`HERMES_TRADING_TIMEZONE` shell env → profile `.env` → preset YAML timezone → リテラル `America/Los_Angeles`**。これはラベル専用の override であり、cron 発火時刻は動きません。完全な priority stack は `cron/README.md` を参照。

cron ジョブは `active` として登録されますが、**Hermes gateway が起動していないと自動発火しません**。`cron list` で4ジョブ確認後にどちらかを選択:

```bash
# A) 常駐サービスとして起動 (本番運用向け推奨)
trading-research-assistant gateway install
trading-research-assistant gateway start

# B) 手動実行のみ (auto-fire させず、cron run で個別実行)
for jid in $(trading-research-assistant cron list | awk '/^  [a-f0-9]{12}/ {print $1}'); do
  trading-research-assistant cron pause "$jid"
done
```

スケジュール待ちせずジョブをドッグフードする:

```bash
# v0.14.0 では `chat -q '/pre-market-routine'` は session_id しか返さないため
# 実出力確認には cron run + cron tick を使う:
trading-research-assistant cron run <pre_market_job_id> --accept-hooks
trading-research-assistant cron tick --accept-hooks
ls ~/.hermes/profiles/trading-research-assistant/cron/output/<pre_market_job_id>/
```

### タイムゾーンの扱い (重要)

Hermes v0.14.0 の `cron create` には **`--tz` フラグが存在しません**。cron expression は **実行ホストのローカル timezone** で解釈されます。`HERMES_TRADING_TIMEZONE` 環境変数はレポート本文用のラベルで、cron の発火時刻には影響しません。

デフォルトスケジュール (PT 想定) を意図通り発火させるには:
- ホスト OS の timezone を `America/Los_Angeles` に揃える、または
- `data/schedule-presets.yaml` の cron expression をホスト timezone に再計算する (runtime が直接読み込むため、スクリプトの編集は不要)

詳細は `cron/README.md` と `docs/03-hermes-compatibility-notes.md`。

---

## バージョニングと再現可能なインストール

Hermes Profile Distribution の install (`hermes profile install github.com/<owner>/<repo>`) は現状、リポジトリの **default branch** を追跡する仕様で、特定タグの pinning には対応していません。GitHub Releases は changelog 用で、最新版は https://github.com/tradermonty/hermes-trading-research-agent-work-package/releases を参照してください。`github.com/...#<tag>` のような ref 指定はまだ Hermes installer には未実装です。

特定の release を再現可能な形で install したい場合は、ローカル clone → tag checkout → ディレクトリから install してください:

```bash
git clone https://github.com/tradermonty/hermes-trading-research-agent-work-package.git
cd hermes-trading-research-agent-work-package
git checkout v0.1.6   # または `git tag -l` で得られる任意の tag
hermes profile install "$(pwd)" --name trading-research-assistant --alias -y
```

Hermes 側で Git-ref pinning が追加されたら、このセクションは GitHub ref 直指定の形に置き換えます。

## MCP サーバ

`mcp.json` はデフォルトで **空** です。将来の Hermes が active MCP config source として明文化するまでは空のままにしてください。Hermes v0.14.0 で確認済みの MCP CLI 経路は `hermes mcp add ...` で、profile の `config.yaml` に `mcp_servers:` として保存されます。例示用の `mcp.example.json` は placeholder/reference のみで、パッケージ名 / 実行コマンド / 権限はすべて、実際に使う MCP server に対して確認が必要です。

推奨: `mcp.json` は空のまま、実サーバは `hermes mcp add ...` または明示的な `config.yaml:mcp_servers` で追加し、cron から見える tool surface を絞る場合は `hermes tools enable/disable --platform cron ...` を使ってください。

## できないこと

- 自動発注は一切しません。
- 利益保証はしません。
- シグナル配信サービスではありません。
- ユーザーが明示的に paper / read-only Alpaca キーを設定する以外、live ブローカー資格情報を扱いません。
- 隠し cron ジョブはありません。すべて `data/schedule-presets.yaml` に明記され、`cron/create_cron_jobs.sh` (`cron/create_cron_jobs.py` の thin wrapper) を明示的に実行した時のみ作成されます。

---

## 重要な受け入れ基準

新規ユーザーが profile install と `.env` 設定だけ済ませて以下を実行できれば成功です:

```text
/pre-market-routine
```

アシスタントは、ユーザーが個別 skill を覚えなくても、必要な Claude Trading Skills を組み合わせて構造化されたリサーチブリーフを出力します。すべての出力セクションは明示的な「人間の最終判断ゲート」で締めくくられます。

---

## 詳細ドキュメント

- `docs/01-architecture.md` — システム構成と責任分担
- `docs/03-hermes-compatibility-notes.md` — Hermes v0.14.0 検証結果 (threat scanner `deception_hide` 回避、timezone 仕様)
- `docs/04-skill-integration-strategy.md` — degraded mode 規則、bundle 命名
- `docs/07-testing-acceptance-criteria.md` — 各テスト層が保証する内容
- `docs/08-release-playbook.md` — リリース前チェックリスト
- `CHANGELOG.md` — バージョン履歴
- `README.md` — English version
