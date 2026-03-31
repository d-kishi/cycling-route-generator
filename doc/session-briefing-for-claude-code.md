# セッション要約: ハーネスエンジニアリング学習とプロジェクト準備

## このドキュメントの目的

claude.aiでの複数回にわたる対話セッション（2026年3月末〜4月）の要約である。新規プロジェクト開始にあたり、Claude Code CLIでの開発に背景情報を引き継ぐために作成した。

---

## ユーザのプロフィール

- アプリケーションエンジニア。C# MVC/.NET + Angular経験があり、Node.jsマイクロサービスへの移行を志向
- Claude Codeを主要な開発ツールとして日常的に使用
- 過去にcc-sdd（仕様駆動開発フレームワーク）を試行したが、バッチ的で単調、Agent Teamsを活かせない点に不満があった
- 過去にClaude Codeのハーネス（Skills, Hooks, Rules）構築を試みたが「やりすぎて」うまくいかなかった経験がある
- linterに対して抵抗感がある（好きではない、価値の勉強をしていないと自認）
- レビューにおいて「ミクロまで確認しようとして時間がかかり、モチベーションが下がる」という課題を抱えている
- 対話的実行を好むが、長時間自律実行のトレンドも認識しており、ハイブリッドなアプローチを模索している

---

## 学習した内容の要約

### ハーネスエンジニアリング

AIコーディングエージェントが信頼性の高い成果物を生成し続けるために人間が設計する「制約・ツール・ドキュメント・フィードバックループ」の総体。3つの構成要素がある:

1. **コンテキストエンジニアリング**: エージェントがアクセスできる情報の整備（CLAUDE.md, Skills, docs/）
2. **アーキテクチャ制約**: ルールの機械的強制（Rules, Hooks, CI/CD, テスト）
3. **ガベージコレクション**: ドキュメント陳腐化・制約違反の自動検出と修正

加えて、Anthropicの知見として**Generator/Evaluator分離**（自己評価の甘さへの構造的解決）が重要。

### AI-DLCとの関係

AI-DLC（AWS提唱）は開発ライフサイクル全体の「What/When」フレームワーク。ハーネスエンジニアリングはその「How」にあたる。個人開発で活かすポイント:
- AI計画→人間検証→AI実装の往復サイクル
- フェーズ間のコンテキスト蓄積
- ボルト（時間〜日単位の高速サイクル）での振り返り

### Everything Claude Code（ECC）

参考にすべきは設計パターンであり、コンポーネントそのものではない:
- エージェントの責務分離（汎用より特化）
- 簡潔なDescription
- 目的別のオーケストレーションパターン
- モデルの使い分け（Sonnet中心、Opusはplanner等のみ）

そのまま導入すると過剰。108 Skills, 25 Agents等の規模は個人プロジェクトには不要。

---

## 合意した方針

### 開発アプローチ

- **最小構成から始めて有機的に育てる**。ハーネスを事前に「完成」させない
- **対話的実行と部分的自律実行のハイブリッド**: 主要な意思決定は対話的に行い、Agent Teamsのサブエージェントには明確に定義できるサブタスクを自律的に委譲
- **ボルト単位の振り返り**: 1機能完了ごとにハーネスの改善点を検討。ただし1ボルトにつき改善は1〜2個まで

### レビュー方針

- 機械に任せられる検証は機械に任せる
- 人間のレビューは「意図との整合性」に集中
- コードの実装詳細・フォーマット・命名規則は人間が逐一確認しない

### 機械的制約の段階的導入

- Phase 1: linterは入れず、Evaluatorエージェント（code-reviewer）中心で開始
- Phase 2: 繰り返し発生するミスに対してのみRulesを追加
- Phase 3: 必要性を実感した場合のみlinter等を導入検討

### ハーネスの初期最小構成

- CLAUDE.md: 1ファイル（概要・目的・技術スタック・ディレクトリ構造・開発ルール3〜5項目）
- Rules: 2〜3ファイル（security, testing, git-workflow）
- Agents: 2〜3体（planner[opus], code-reviewer[sonnet], 必要に応じてe2e-tester）
- Hooks: 1〜2個（セッション開始時のコンテキスト読み込み）
- Skills: 0〜2個（繰り返す操作が出てきた時点でSkill化）

---

## 新規プロジェクトの概要

### サイクリングルート自動生成サービス

- **ユーザ入力**: 方角、距離、獲得標高などのパラメータ
- **ルート生成**: 入力に基づき複数のルート候補を自動生成
- **地図表示**: 生成されたルートをGoogleMap的な地図上に表示
- **エクスポート**: .tcx / .gpx形式でダウンロード可能（Strava/Garmin連携用）
- **将来構想**: 走行ルートのシェア、危険箇所やお気に入りポイントの共有（ソーシャル機能）

技術スタックは未決定。これから/initを使って決定していく。

---

## 参照ドキュメント

- `harness-engineering-guide.md`: 詳細版のガイドドキュメント（6章構成）。本ドキュメントと同じセッションで作成
- OpenAI "Harness engineering: leveraging Codex in an agent-first world" (2026/2)
- Anthropic "Effective harnesses for long-running agents"
- Anthropic "Harness design for long-running application development" (2026/3)
- AWS "AI-Driven Development Life Cycle" (2025/8)
- Everything Claude Code (github.com/affaan-m/everything-claude-code)
- claude-code-best-practice (github.com/shanraisshan/claude-code-best-practice)

---

## 次のアクション

1. 技術スタックの決定（/initを活用）
2. CLAUDE.mdの初稿作成
3. 最小ハーネス構成でプロジェクト開始
