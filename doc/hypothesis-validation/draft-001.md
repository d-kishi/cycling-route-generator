# 仮説キャンバス Draft 001

- 作成日: 2026-05-02
- 作成者: メインAgent(開発チームリーダー) + PO
- 状態: debate前のキャンバス骨格

## 立案経緯

- 前回(2026-04-09)の仮説キャンバスv1は2026-04-23にPOが手動削除済み(要点は memory `project_previous_hypothesis.md` に保存)
- Step A(2026-05-01)で5体ペルソナを形成完了。各ペルソナの broadlistening_summary に一次情報のエビデンスを保有
- Step B(2026-05-02)で `/spec-hypothesis` SKILL.md を改修し、persona-<id>.yaml 全文を Round 1 で渡す設計に変更
- Step C 開始時に PO 判断: 5体すべてを debate 参加メンバーとする(コンテキスト容量1Mで余裕、参加密度優先)
- root は案B(多層化拡張)を採用。各層の固有困難を明示する文言で5体全員にアンカーを提供

## 参加ペルソナ(5体)

| ID | 名前 | 月間距離 | 主な動機 |
|---|---|---|---|
| persona-hobby | 中級ホビーロードサイクリスト | 500km | 走り続ける楽しさ、新景色 |
| persona-beginner | ビギナーロードサイクリスト | 100-200km | 健康維持、趣味づくり |
| persona-serious | シリアスロードライダー | 1000-1500km | FTP向上、レース成績 |
| persona-casual | カジュアルスポーツバイク乗り | 50-150km | 観光、グルメ、移動 |
| persona-endurance | ロングライド/ブルベライダー | 800-1500km | 完走達成感、SR取得 |

## 仮説の根源(root) — 多層化拡張版

```
サイクリストは自分の目的・経験・走行スタイルに合うルートを継続的に得るのが難しい。
中級層は目的地枯渇、初心者は安全性・道迷い不安、ロング志向は補給計画、
競技志向は練習ルート設計、カジュアル層はテーマ起点探索など、
層ごとに異なる困難を抱えるが、それを束ねる手段が存在しない。
```

### 採用根拠

- Step A収集データで各層の固有困難が裏付けられている(下記キャンバスのevidence参照)
- 5体全員参加のためアンカーが各ペルソナに対して機能する必要があり、hobby起点の前回rootでは4体がroot外と感じるリスクがあった
- 「層を束ねる手段が存在しない」という横断的課題認識を debate のアンカーに据える

### リスクと対応

- 議論拡散リスクあり(案B選択時の既知リスク)
- 対応: ファシリテータが Round 1 のアイデア収集後、層別の論点を整理してから Round 2 に進む

---

## キャンバス案(YAML骨格)

```yaml
meta:
  project: "サイクリングルート自動生成サービス"
  version: 1
  updated: "2026-05-02"
  phase: "draft"

root:
  type: "課題"
  statement: |
    サイクリストは自分の目的・経験・走行スタイルに合うルートを継続的に得るのが難しい。
    中級層は目的地枯渇、初心者は安全性・道迷い不安、ロング志向は補給計画、
    競技志向は練習ルート設計、カジュアル層はテーマ起点探索など、
    層ごとに異なる困難を抱えるが、それを束ねる手段が存在しない。
  rationale: |
    Step A(2026-05-01)で形成した5体ペルソナの broadlistening_summary に
    各層の固有困難が一次情報として記録されている。
    PO自身は中級ホビー(persona-hobby)層に該当し、目的地枯渇を実体験している。

canvas:

  # ===========================
  # 顧客/ユーザ側
  # ===========================
  customer:

    situation:
      id: C-SIT
      title: "層ごとに異なるルート選択コスト"
      hypothesis: |
        サイクリストは経験レベル・走行スタイル・所属コミュニティに応じて、
        ルート選択に異なる時間コストと認知コストを払っている。
        中級層: 週末ライドのルート選びに30分-1時間
        初心者: 経験者同行 or 慣れた範囲のみ走行可能
        競技層: 練習目的に応じた区間設計が必要
        カジュアル層: テーマ・目的地を軸に毎回手動探索
        ロング志向: 200km超のPC・補給・宿泊計画が完走条件
      confidence: medium
      evidence:
        - source: "Step A 5体ペルソナの typical_scenario / supply_planning_practice"
          detail: ".claude/personas/persona-*.yaml の attributes に各層の状況が記録"

    overt_problem:
      id: C-OVR
      title: "同じルートの繰り返しに飽きる(中級層)"
      hypothesis: |
        中級ホビー層は気に入ったルートを繰り返し走るうちにマンネリ化し、
        新しいルートの開拓は手動探索に依存しているため、
        アイデアが枯渇すると行き詰まる。
      confidence: medium
      evidence:
        - source: "PistonHeads UK (2024)"
          detail: "I love exploring but am getting to a point where there's not much I haven't explored locally (Correvor氏)"
        - source: "BikeForums (2019)"
          detail: "the thought of doing the same ride/route takes the joy out of it (mcours2006氏)"
        - source: "PO実体験"
          detail: "週末ライドで感じている目的地枯渇"

    overt_problem_safety:
      id: C-OVR-SFT
      title: "安全ルート不安と道迷い恐怖(初心者層)"
      hypothesis: |
        初心者は車道走行・道迷い・パンク等への恐怖から、
        経験者同行か自宅周辺の慣れた範囲しか走行できず、行動範囲が広がらない。
      confidence: medium
      evidence:
        - source: "Yahoo!知恵袋 / ryusuke-tax.com (2020)"
          detail: "1人で走行するのって、凄く怖いです / 地名を知らないと迷う"
        - source: "bicycle-post.jp"
          detail: "一人だと心が折れてしまう傾向、経験者同行への依存強い"

    overt_problem_supply:
      id: C-OVR-SUP
      title: "補給・PC計画の手動マッピング負荷(ロング志向)"
      hypothesis: |
        ロング志向は200km超のライドで、コンビニ間隔・自販機・道の駅営業時間・
        PC位置・エスケープ地点・宿泊先を事前に手動マッピングする必要があり、
        これがDNF回避の鍵だが膨大な計画工数を要する。
      confidence: medium
      evidence:
        - source: "Audax Japan公式"
          detail: "BRMは無サポート・回収車なし・自己責任。キューシート自力読解前提"
        - source: "pbpresults.com / cyclecharts.uk"
          detail: "PBP 2023: 全66カ国6,430名出走、DNF 80%以上が2日目までに発生"

    overt_problem_training:
      id: C-OVR-TRN
      title: "練習目的別ルート設計の手間(競技志向)"
      hypothesis: |
        競技志向は練習目的(VO2max・FTP・スプリント・ヒルクライム試走)に応じて
        毎回異なる勾配・距離・路面のルート設計が必要だが、
        既存ツールはトレーニング計画と独立しており連携がない。
      confidence: low
      evidence:
        - source: "note.com"
          detail: "1年以上225WでFTPが頭打ち / 無計画トレーニング / VO2max効果は6-8週間で飽和"
        - source: "Red Bull・専門メディア"
          detail: "適切な強度管理欠如、トレーニング計画の体系性不足"

    overt_problem_theme:
      id: C-OVR-THM
      title: "テーマ起点のルート探索手段不足(カジュアル層)"
      hypothesis: |
        カジュアル層は「お花見ライド」「グルメ巡り」「御朱印」「廃線跡」など
        テーマ起点でルートを組みたいが、Googleマップ自転車モードでは
        テーマと自転車適性を両立した探索ができず、毎回手動で組み直している。
      confidence: low
      evidence:
        - source: "Toy Bike等のテーマ設定型ライド事例"
          detail: "お花見ライド、グルメライド等のテーマ起点ライド文化が存在"
        - source: "persona-casual parallel_hobbies"
          detail: "観光・地理探索系/グルメ・体験系/旅行・移動系の3カテゴリで自転車を『手段』として使う"

    latent_problem:
      id: C-LAT
      title: "層を横断する『自分用ルートの不在』"
      hypothesis: |
        各層に共通する潜在課題は、自分の状況・目的・走行スタイルに合うルートが
        自分用にカスタマイズされた形で得られないこと。
        標準化されたコース集や他人のログを参考にするしかなく、
        『自分のためのルート提案』を受け取る体験が存在しない。
      confidence: low
      evidence: []

    alternatives:
      id: C-ALT
      title: "Strava/RideWithGPS/Komoot/Googleマップ等の併用"
      hypothesis: |
        現在は層ごとに異なるツール(Strava, RideWithGPS, Komoot, Garmin Connect,
        Googleマップ自転車モード, 個人ブログ, ガイド本)を使い分けているが、
        『自分の条件・目的・層特性に合ったルートを自動生成』する横断的手段はない。
      confidence: medium
      evidence:
        - source: "Step A 各ペルソナの navigation_tool"
          detail: "層ごとに異なるツール組み合わせが定着している"

  # ===========================
  # 提供者側
  # ===========================
  provider:

    purpose:
      id: P-PUR
      title: "層を問わず最小入力で満足ルートを得る"
      hypothesis: |
        サイクリストが層を問わず「今日はこういう走りがしたい」と思った時に、
        層ごとの固有要件(安全性・補給・練習設計・テーマ等)を考慮した
        満足できるルートを最小入力で手に入れられる状態を作る。
      confidence: low
      evidence:
        - source: "PO自身のペイン"
          detail: "毎週末のルート選びに感じるフラストレーション"

    vision:
      id: P-VIS
      title: "走ることに集中できる世界"
      hypothesis: |
        サイクリストが走ることそのものに集中できる世界。
        ルート計画の手間をゼロに近づけ、層に関わらず
        『自分のためのルート提案』を受け取れるようにする。
      confidence: low
      evidence: []

    proposed_value:
      id: P-VAL
      title: "層別パラメータでの自動ルート生成と地図比較"
      hypothesis: |
        方角・距離・獲得標高に加え、層別の固有パラメータ
        (安全性重視、補給ポイント密度、勾配パターン、テーマ等)を組み合わせて、
        複数のルート候補を自動生成し、地図上で比較できる。
      confidence: low
      evidence:
        - source: "技術調査"
          detail: "BRouterのカスタムプロファイル機能で層別パラメータ実装可能"

    solution:
      id: P-SOL
      title: "BRouter+Leaflet Webアプリ + 層別プロファイル + エクスポート"
      hypothesis: |
        BRouterのカスタムプロファイル機能で層別の最適化を実現し、
        Leaflet地図上に複数候補を表示。.tcx/.gpx形式でエクスポート可能。
        層別プロファイルは MVP では中級層から開始し、debateの結果に応じて
        他層の優先順を決定する。
      confidence: medium
      evidence:
        - source: "技術調査"
          detail: "BRouter + Leaflet + OpenStreetMapで層別プロファイル実装可能"

    advantage:
      id: P-ADV
      title: "PO=hobby層 + BRouterセルフホスト + 層別差別化"
      hypothesis: |
        PO自身がhobby層であり、実体験に基づくフィードバックを高速で回せる。
        BRouterセルフホストにより層別カスタムプロファイルの自由度が高い。
        他ツールが特定層中心(StravaはKOM狙い、Komootはツーリング志向等)なのに対し、
        本サービスは層別差別化で広いペルソナをカバーする点が差別化要因。
      confidence: low
      evidence: []

  # ===========================
  # ビジネス側(任意。今回は未検討)
  # ===========================
  business:
    channel: null
    metrics: null
    revenue: null
    market_size: null

# --- 仮説間のリレーション ---
relations:
  # 各層の状況(C-SIT) → 各層の顕在課題
  - from: C-SIT
    to: C-OVR
    type: supports
    note: "中級層の状況がマンネリ課題を生む"
  - from: C-SIT
    to: C-OVR-SFT
    type: supports
    note: "初心者層の状況が安全不安課題を生む"
  - from: C-SIT
    to: C-OVR-SUP
    type: supports
    note: "ロング志向の状況が補給計画課題を生む"
  - from: C-SIT
    to: C-OVR-TRN
    type: supports
    note: "競技層の状況が練習設計課題を生む"
  - from: C-SIT
    to: C-OVR-THM
    type: supports
    note: "カジュアル層の状況がテーマ起点探索課題を生む"

  # 顕在課題群 → 横断的潜在課題
  - from: C-OVR
    to: C-LAT
    type: derives
    note: "中級層のマンネリは『自分用ルート不在』の現れ"
  - from: C-OVR-SFT
    to: C-LAT
    type: derives
    note: "初心者の安全不安も『自分用ルート不在』の現れ"
  - from: C-OVR-SUP
    to: C-LAT
    type: derives
    note: "ロング志向の補給計画手間も『自分用ルート不在』の現れ"
  - from: C-OVR-TRN
    to: C-LAT
    type: derives
    note: "競技層の練習設計手間も『自分用ルート不在』の現れ"
  - from: C-OVR-THM
    to: C-LAT
    type: derives
    note: "カジュアル層のテーマ起点不在も『自分用ルート不在』の現れ"

  # 潜在課題 → 目的・提案価値
  - from: C-LAT
    to: P-PUR
    type: derives
    note: "横断的潜在課題から目的が導出される"
  - from: C-LAT
    to: P-VAL
    type: derives
    note: "潜在課題が層別パラメータ自動生成の価値を裏付ける"

  # 代替手段 → 提案価値
  - from: C-ALT
    to: P-VAL
    type: supports
    note: "既存手段では横断的・層別自動生成ができないことが提案価値の差別化根拠"

  # 目的 → ビジョン
  - from: P-PUR
    to: P-VIS
    type: derives
    note: "目的の延長線上にビジョンがある"

  # 提案価値 → ソリューション
  - from: P-VAL
    to: P-SOL
    type: derives
    note: "層別パラメータをBRouterカスタムプロファイルで実現"

  # 優位性 → ソリューション
  - from: P-ADV
    to: P-SOL
    type: supports
    note: "PO実体験+セルフホストで実装の自由度確保"
```

---

## 設計判断(メインAgent=開発チームリーダー視点)

1. **顕在課題を層別に5分割した理由**: rootが多層化されたため、顕在課題も層別に明示しないと debate で各ペルソナが「自分の課題」を見つけにくい。debate中に層別仮説が深掘られたら、追加の hypothesis として吸収する。
2. **C-LAT(横断潜在課題)を設置した理由**: 5層の顕在課題を束ねる「自分用ルートの不在」というアンカーを提供。これが provider 側の P-PUR / P-VAL を導出する根拠となる。
3. **P-VAL を「層別パラメータ自動生成」と表現した理由**: 単なる方角・距離・獲得標高生成では他ツールとの差別化が弱い。層別パラメータ(安全性、補給、勾配、テーマ等)の組み合わせを軸に据えることで、5層全員にとっての価値を表現できる。
4. **MVP範囲は debate 後に決定**: P-SOL の hypothesis 内に「MVP では中級層から開始」と記載したが、debate で層別優先順位が変わる可能性があるため確定はしない。
5. **business 区画は未検討**: 個人開発のためビジネス側は debate 対象外。

---

## debateで深掘りすべき論点(事前抽出)

各ペルソナの broadlistening_summary を踏まえると、以下の論点が想定される。Round 1 のアイデア出しでこれらが自発的に出てくるか、新たな視点が加わるかを観察する。

| 論点 | 想定対立軸 |
|---|---|
| パラメータ起点 vs テーマ起点のルート生成 | hobby/serious(パラメータ) vs casual(テーマ) |
| 補給ポイント情報マッピング | endurance(必須) vs hobby(あれば便利) vs beginner(コンビニ位置で十分) |
| ツール一元化 vs 複数ツール併用 | beginner/casual(一元化) vs serious/endurance(専門ツール併用) |
| ロード文化前提 vs ロード文化外 | hobby/serious/endurance(Strava前提) vs casual(Strava不使用) |
| 安全性パラメータの定義 | beginner(車両通行少なさ) vs hobby(平坦+軽登り) vs serious(信号少なさ) |
| 練習目的別の路面・勾配設計 | serious 固有の論点 |
| 機材投資文化差(完成車5万 vs 150万) | casual vs serious |

---

## 次のステップ

- POによる本ドラフトのレビュー: 文言修正・追加すべき視点の指摘を受ける
- 修正後 Step 5(debate Round 1-3)に進む
