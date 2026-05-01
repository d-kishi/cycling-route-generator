---
name: persona
description: ペルソナ(.claude/personas/persona-<id>.yaml)の形成・更新・一覧を行うスキル。ブロードリスニングでペルソナ層の実声を収集し、Generator/Evaluator分離と計算的Sensorsで品質を担保する。スラッシュコマンド `/persona` で起動する。
model: opus
disable-model-invocation: true
---

# persona: ペルソナ形成スキル

## このスキルの目的

1人のエンジニアの視野では見落とされがちな多様な視点を、ブロードリスニングで得られる実ユーザ層の声を取り込んだペルソナとして具体化する。
形成されたペルソナは `/spec-hypothesis` のdebate、デザインレビュー、将来の別プロジェクトなどで再利用できる独立した成果物である。

本スキルは以下2点を仕組みで担保する:

- **Generator/Evaluator分離**: Collector SubAgentが情報を集め、Evaluator SubAgentが品質を評価する。確証バイアスを構造的に排除する
- **計算的Sensors**: LLM判断に依存しない決定論的な検証をワークフローの要所に配置し、品質の下限を保証する

## 呼び出しパターン

| コマンド | 動作 |
|---|---|
| `/persona` | 新規ペルソナ形成（対話→チェックリスト→Collector-Evaluatorループ→形成） |
| `/persona update` | 既存ペルソナの更新（情報の追加・細分化） |
| `/persona list` | 形成済みペルソナ一覧の表示 |

---

## Guides: 良いペルソナの6基準

ペルソナを形成・更新する際、以下の基準を満たすかを常にチェックする。
SubAgent起動時にもこの基準を伝える。

1. **明確な差別化**: 他のペルソナと役割・視点が重複していない
2. **具体性**: 抽象的でない（「サイクリスト」ではなく「週末に30km走るロード初心者」のレベル）
3. **一次情報の反映**:
   - 実在するユーザ層から得られる声・データに基づいて形成する
   - 推測や想像だけで構築しない
   - 直接的な一次情報が得られない場合:
     - 著名な発信者（YouTuber、ブロガー等）を参照することは可。ただし1人に依存せず、複数の発信者や情報源から要素を抽出する
     - 抽出した要素は統合・抽象化し、特定個人のコピーではなく「その層を代表するアーキタイプ」として形成する
     - 発信者は平均的ユーザではない（発信力のある特殊層）ことを認識し、そのバイアスを補正する
4. **内部整合性**: 属性間に矛盾がない（例: 「初心者」と「レース経験豊富」の併存は不可）
5. **ドメイン適合性**: プロジェクトの文脈で意味のある視点を提供できる
6. **情報源の多様性**: 複数の情報源から形成され、1つに偏らない

---

## Guides: ブロードリスニングの情報源優先順位

Collector SubAgentには以下の優先順位に沿って情報を収集させる。

| 優先度 | 情報源 | 特徴 |
|---|---|---|
| 高 | 公式・一次情報（公式サイト、公的調査、専門メディア） | 信頼性最高 |
| 中 | 専門コミュニティ（Reddit特定スレッド、専門フォーラム） | 実ユーザーの声、濃い情報 |
| 中 | SNS（X、Strava等、日本語圏含む） | リアルタイム性、ユーザの本音 |
| 低 | 一般ブログ、個人ブログ | バイアスあり、補助的 |
| 除外 | アフィリエイトサイト、SEO対策コンテンツ | ノイズが多い |

---

## Guides: ペルソナYAMLスキーマ

成果物は `.claude/personas/persona-<id>.yaml` に保存する。
最低限の必須フィールドは以下。

```yaml
id: string                       # 必須、ユニーク（kebab-case推奨）
name: string                     # 必須、ペルソナの通称
description: string              # 必須、1-2行の説明
attributes:                      # 必須、最低1項目
  age_range: string              # 例: "30代後半"
  experience_level: string       # 例: "ロード歴3年、週末ライダー"
  typical_scenario: string       # 例: "土日に都内発60-80km"
  motivation: string             # 例: "景色の変化と健康維持"
  # 追加の属性は自由
checklist:                       # 必須、最低1項目
  - category: string             # 収集すべき情報カテゴリ名
    rationale: string            # なぜ収集するか
    queries:                     # 検索の起点となるキーワード/質問
      - string
broadlistening_summary:          # 充実化後に必須
  - category: string             # checklist.category と対応
    summary: string              # Collectorの要約
    sources:                     # 参照した情報源
      - url: string
        type: primary | community | sns | blog
        note: string             # 補足（誰の声か、どのくらい信頼できるか等）
    self_assessment:             # Collectorの自己評価（参考）
      coverage: high | medium | low
      confidence: high | medium | low
      notes: string
created_at: date                 # 必須、YYYY-MM-DD
last_updated: date               # 必須、YYYY-MM-DD（ドリフト検出用）
```

---

## 新規作成ワークフロー (`/persona`)

### Step 1: プロジェクトコンテキストの収集

`CLAUDE.md` と `doc/` 配下、および既存の `.claude/personas/` 配下を読み、プロジェクトの現状と既存ペルソナ構成を把握する。

### Step 2: ペルソナ内容とチェックリストの対話形成

POと対話し、以下を決める:

- ペルソナのid（`.claude/personas/persona-<id>.yaml` のファイル名になる）
- name / description / attributes
- チェックリスト（ブロードリスニングで収集すべき情報カテゴリ）
  - 初回は粗い粒度でよい。
    Collector-Evaluatorループ中に必要に応じて細分化する
  - 各カテゴリに `rationale` と `queries` を必ず付ける

チェックリストの例:

```yaml
checklist:
  - category: "週末ライドの不満"
    rationale: "課題仮説の妥当性検証"
    queries:
      - "ロードバイク 週末 マンネリ"
      - "サイクリングルート 飽きた"
  - category: "ルート選びの実践"
    rationale: "どのツール・情報源を使っているか把握"
    queries:
      - "Strava ルート作成"
      - "Googleマップ 自転車 使いにくい"
```

### Step 3: [Sensor] ID重複チェック

`references/sensors/check_id_uniqueness.py` を呼び出し、新規作成しようとしているidが既存ペルソナと衝突していないかを検証する。

- 失敗時: エラーメッセージを提示し、POにid変更を求める
- 成功時: 次ステップへ

### Step 4: ファイル保存（初期状態）

Step 2で決めた内容を `.claude/personas/persona-<id>.yaml` として保存する。
この時点では `broadlistening_summary` は未記入。

### Step 5: [Sensor] YAMLスキーマ検証

`references/sensors/validate_schema.py` を呼び出し、保存したYAMLが必須フィールドを満たしているかを検証する。

- 失敗時: エラーメッセージを提示し、手動修正を促す
- 成功時: 次ステップへ

### Step 6: Collector-Evaluator ループ（最大3回）

以下を最大3回繰り返す。

#### 6.1 Collector SubAgent 起動

`subagent_type: persona-collector` で起動する。
渡す情報:

- 対象ペルソナのYAML全文（attributes, checklist を含む）
- 「良いペルソナの6基準」
- 「情報源優先順位」
- ループ回数（2回目以降はEvaluatorの前回指摘も含める）

Collectorは「収集→即要約→生データ破棄→次の収集」の逐次処理を行い、全カテゴリの要約・情報源・自己評価を返す。

#### 6.2 [Sensor] チェックリスト完全性チェック

`references/sensors/check_checklist_completeness.py` を呼び出し、Collector返却値の `results[].category` が、対象ペルソナYAMLの `checklist[].category` と完全一致するかを機械的に検証する。
配置: Collector返却直後。

呼び出し方:
1. Collector返却YAMLを一時ファイル（例: `$TMPDIR/collector_output.yaml`）に保存
2. `python3 .claude/skills/persona/references/sensors/check_checklist_completeness.py <persona_yaml> <collector_output_yaml>`

検出する不一致:

- **欠落カテゴリ**: ペルソナにあるがCollectorが返さなかったカテゴリ
- **不要カテゴリ**: ペルソナにないのにCollectorが追加した/誤名を作ったカテゴリ
- **順序不一致**: 共通カテゴリの順序がペルソナYAMLと異なる

失敗時の対応:

- 欠落のみ（残ループあり）: 不足カテゴリを指示してCollectorに再投入
- 不要・誤名あり（残ループあり）: カテゴリ名厳守を指示してCollectorに再投入
- 残ループなし or 内容自体は有用: メインAgentが手動でマッピング・統合し、再度Sensor 6.2を通す
- いずれの場合も次ループでカテゴリ名を厳守させること（persona-collector.md に厳守ルール明記済み）

#### 6.3 [Sensor] 情報源URL有効性チェック（将来拡張）

Collector返却値のsource URLの到達性を確認する（注: ネットワーク依存のため初期実装では警告のみ、または未実装）。

#### 6.4 Evaluator SubAgent 起動

`subagent_type: persona-evaluator` で起動する。
渡す情報:

- Collectorの返却値全文
- 対象ペルソナのYAML
- 「良いペルソナの6基準」

Evaluatorは以下の観点で判定する:

- 情報源の多様性（1種類のソースに偏っていないか）
- 具体性（抽象論ではなく具体的なエピソード・声があるか）
- 一次情報の含有率
- カテゴリ間の情報バランス

判定結果は `pass | fail` + 理由 + 追加収集方針（failの場合）で返される。

#### 6.5 ループ終了判定

- Evaluatorが `pass` → ループを抜けてStep 7へ
- Evaluatorが `fail` かつ ループ残あり → 追加収集方針をCollectorに渡して再ループ
- Evaluatorが `fail` かつ ループ上限到達 → ここで打ち切り、Step 7に進む前にPOに判断を仰ぐ

### Step 7: ペルソナ充実化

Evaluator承認済みの要約を `broadlistening_summary` に統合してYAMLを更新する。
`last_updated` を当日日付に更新する。

### Step 8: [Sensor] 必須フィールド有無チェック

`references/sensors/check_required_fields.py` を呼び出し、充実化後のYAMLが `broadlistening_summary` を含む全必須フィールドを満たしているかを検証する。

- 失敗時: 不足フィールドを提示して手動修正を促す
- 成功時: 次ステップへ

### Step 9: PO承認（オプション）

充実化されたペルソナをPOに提示し、承認を得る。
デフォルトは自動進行だが、初期段階では明示確認を推奨する。

- 承認 → 完了
- 要修正 → POの指示に従い該当箇所を更新し、再度 Step 8 から流す

---

## 更新ワークフロー (`/persona update`)

### Step 1: 既存ペルソナの読み込み

`.claude/personas/` 配下の一覧を提示し、更新対象をPOに選ばせる。
対象YAMLを読み込む。

### Step 2: 更新トリガーの確認

POに更新理由を尋ねる。
例:

- 情報が古くなった（ドリフト検出）
- チェックリストを細分化したい
- 追加カテゴリを追加したい

### Step 3: チェックリストの見直し

必要に応じて以下を行う:

- 既存カテゴリの細分化
- 新規カテゴリの追加
- 既存カテゴリのqueryの更新

### Step 4: Collector-Evaluator ループ

新規作成のStep 6と同じ。
ただし既存の `broadlistening_summary` との差分のみ収集するよう Collector に指示できる。

### Step 5: 充実化とSensor検証

新規作成のStep 7-8と同じ。
`last_updated` を当日日付に更新する。

---

## 一覧ワークフロー (`/persona list`)

`.claude/personas/` 配下の全YAMLを読み、以下のサマリーを表として表示する。

| id | name | description | last_updated | カテゴリ数 |
|---|---|---|---|---|

詳細（attributes, broadlistening_summary全文）は表示しない。
必要な場合はPOが該当YAMLを直接読む。

---

## Sensors一覧

LLM判断に依存しない機械的な品質下限を保証する。

| Sensor | 対象 | 配置タイミング | 失敗時の挙動 | スクリプト |
|---|---|---|---|---|
| ペルソナID重複チェック | ペルソナYAML | 新規作成前（ファイル保存前） | エラー表示、ID変更を求める | `references/sensors/check_id_uniqueness.py` |
| YAMLスキーマ検証 | ペルソナYAML | ファイル保存直後 | エラー表示、手動修正 | `references/sensors/validate_schema.py` |
| チェックリスト完全性 | Collector成果物 | Collector返却直後 | 不足/誤名/不要カテゴリを提示、再収集 or 手動マッピング | `references/sensors/check_checklist_completeness.py` |
| 情報源URL有効性 | Collector成果物 | Evaluator前 | 死にリンクをフラグ、警告のみ | 初期未実装（将来拡張） |
| 必須フィールド有無 | ペルソナYAML | 充実化後 | エラー表示、手動修正 | `references/sensors/check_required_fields.py` |

Sensorsスクリプトは全てPython標準ライブラリ + pyyaml のみで実装する。

---

## ファイル配置

```
.claude/
├── personas/                       # ペルソナ成果物（利用側プロジェクト固有）
│   ├── persona-<id>.yaml
│   └── ...
├── skills/
│   └── persona/                    # Skill定義（Plugin配布対象）
│       ├── SKILL.md
│       └── references/
│           └── sensors/            # 計算的Sensors
│               ├── check_id_uniqueness.py
│               ├── validate_schema.py
│               └── check_required_fields.py
└── agents/                         # SubAgent定義（Plugin配布対象）
    ├── persona-collector.md
    └── persona-evaluator.md
```

---

## 注意事項

- ペルソナの記述言語は日本語
- id は安定IDとして扱う。
  削除時は欠番を許容する
- 1回の実行で完璧なペルソナを目指さない。
  `update` で段階的に精緻化する
- Collector SubAgentの逐次処理（収集→即要約→破棄）は200kコンテキスト制限への対策として必須。
  まとめて収集してから要約する形には絶対にしない
- Collector/Evaluator両SubAgentは `memory: user` スコープを持つ。
  メタ知識（情報源の見つかりやすさ、評価基準の精緻化等）はドメイン非依存であり、Plugin公開時に利用者の学習が継続する
- ドリフト検出は初期実装では `last_updated` フィールドのみ。
  機械的検出は GitHub Issue #3 を参照（Plugin公開時に実装予定）
