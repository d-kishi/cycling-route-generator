---
description: Gitワークフローとコミット規約。git操作時に適用。
---

- mainブランチに直接コミットしない。feature/*ブランチで開発しPRでマージする
- コミットメッセージはConventional Commits形式: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`
- worktreeでの並列開発を想定。ブランチ名は機能を明確に示す命名にする（例: `feature/route-generation`, `feature/map-ui`）
