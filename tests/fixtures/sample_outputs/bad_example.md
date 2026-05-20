# Pre-market routine — bad example for negative test

This file exists ONLY to verify that tests/test_output_safety.py catches
prohibited execution language. It must intentionally contain forbidden
patterns from both EN_FORBIDDEN and JA_FORBIDDEN. Do NOT use as a template.

## Bad calls

- Buy at $145.00 immediately.
- Sell at $120 if it taps.
- Place a market order on AVGO open.
- This is a guaranteed profit setup.

## 日本語の悪い例

- 成行で買え。
- 今すぐ買い。
- 全力で入れ。
- 必ず勝てる場面。
- 利益確定でリスクオフ完了。
