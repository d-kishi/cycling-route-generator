# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

サイクリングルート自動生成サービス。ユーザが方角・距離・獲得標高などのパラメータを入力し、複数のルート候補を自動生成して地図上に表示する。.tcx/.gpx形式でエクスポート可能。

詳細は @doc/session-briefing-for-claude-code.md を参照。

## 技術スタック

- **モノレポ**: Nx
- **バックエンド**: NestJS (TypeScript)
- **フロントエンド**: Angular (TypeScript)
- **地図**: Leaflet + OpenStreetMap
- **ルーティングエンジン**: BRouter (セルフホスト)
- **設計思想**: DDD。モノリスから開始し、将来的なマイクロサービス分割を考慮。Nxライブラリ境界 ≒ バウンデッドコンテキスト

## Gitワークフロー

- `main` = 安定ブランチ。直接コミットしない
- `feature/*` = 開発ブランチ。worktreeで並列開発可能
- PRでmainにマージ（code-reviewerエージェントがレビュー）
- コミットメッセージ: Conventional Commits (`feat:` / `fix:` / `chore:` / `docs:` / `refactor:` / `test:`)

## プロジェクト重要目標

- **仮説検証型アジャイルのClaude Code実現**: 市谷聡啓「正しいものを正しく作る」で提示されている仮説検証型アジャイル（特に仮説キャンバス）を、Claude Codeとの協同で実践する。製造前の工程（仮説キャンバス → EARS要件定義 → ドメインモデル）をSkills等で仕組み化し、「正しいものを探す」プロセスをAIエージェントと共に回す

## 開発原則

- 最小構成から始めて有機的に育てる。事前に「完成」させない
- 対話的実行と部分的自律実行のハイブリッド: 主要な意思決定は対話的に行い、明確なサブタスクはAgent Teamsに委譲
- 1ボルト（機能単位の完了サイクル）ごとにハーネスの改善点を検討。ただし1ボルトにつき改善は1〜2個まで

## テスト方針

ハイブリッドTDD:
- API・ビジネスロジック: テスト先行（TDD）
- UI・フロントエンド: 実装後にテスト追加

機械に任せられる検証（テスト、型チェック）は機械に任せ、人間のレビューは「意図との整合性」に集中する。

## レビュー方針

- コードの実装詳細・フォーマット・命名規則は人間が逐一確認しない
- Evaluatorエージェント（code-reviewer）が通せる品質チェックは人間が見ない
- 人間は「自分が望んだものになっているか」だけを判断する

## ハーネスの段階的導入

現在Phase 1: linterなし、Evaluatorエージェント中心で開始。
繰り返し発生するミスに対してのみRules/Hooks/Skillsを追加する。
詳細は @doc/harness-engineering-guide.md を参照。

## ブロードリスニングの技術制約 (`/persona` Collector)

`/persona` スキルの Collector SubAgent はWeb検索・WebFetchで情報収集を行う。以下の制約により、X(旧Twitter)からの直接投稿取得は2026年5月時点で事実上不可能と判明している(persona-hobby 形成時に検証済み)。

- **X API有料化(2023年〜)**: Free tier では検索取得不可。Basic tier 月$100、Pro tier 月$5,000。Claude Code 標準環境では API キーを持たない
- **ログイン要求の壁**: `https://x.com/search?q=...` および個別投稿URLは未認証アクセスでログインページへリダイレクト。WebFetch は認証セッションを持たないためHTML本文取得不可
- **Strava ソーシャル機能**: クラブ掲示板API は非公開。アクティビティコメント取得API は OAuth2 必須(Claude Code 標準環境では認証情報なし)

### 代替アプローチ(本プロジェクトで採用)

- Togetter / Min.t などのXまとめサイト(WebFetch可)
- Reddit / PistonHeads / BikeForums など英語圏専門コミュニティ
- App Store / Google Play レビュー
- Yahoo!知恵袋
- YouTube動画コメント

### Plugin展開時の留意点

本リポジトリの `/persona` スキル一式を Plugin として再利用する場合、利用者側の環境次第ではX API課金・Strava OAuth 認証情報の整備により品質向上の余地がある。逆にFree環境を前提とするなら、Evaluator の判定基準で「SNS直接投稿の必須化」は緩和し、上記代替手段を「SNS的本音の代替」として実質評価する運用が現実的。
