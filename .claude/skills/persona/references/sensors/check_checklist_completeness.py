#!/usr/bin/env python3
"""
check_checklist_completeness.py

Collector成果物のカテゴリ名が、対象ペルソナYAMLの checklist と完全一致するかを検証する。
不一致(欠落・不要・誤名)を機械的に検出する Sensor 6.2 のスクリプト実装。

Usage:
    python3 check_checklist_completeness.py <persona_yaml_path> <collector_output_yaml_path>

Args:
    persona_yaml_path: 対象ペルソナYAMLファイル(checklist[].category が真値)
    collector_output_yaml_path: Collectorが返したYAML(collector_output.results[].category)

Exit codes:
    0: 完全一致(全カテゴリが揃い、誤名・追加なし)
    1: 不一致あり(欠落カテゴリ、誤名カテゴリ、不要カテゴリのいずれか)
    2: 入力エラー(引数不足、ファイル読み込み失敗、構造不正等)
"""
import sys
import os
import yaml


def load_yaml(path: str) -> dict:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"ファイルが見つかりません: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def extract_persona_categories(data: dict) -> list[str]:
    """ペルソナYAMLから checklist[].category を順序保持で抽出"""
    if not isinstance(data, dict):
        raise ValueError("ペルソナYAMLのルートが dict ではありません")
    checklist = data.get("checklist")
    if not isinstance(checklist, list) or len(checklist) == 0:
        raise ValueError("ペルソナYAMLに 'checklist'(非空list) がありません")
    categories: list[str] = []
    for i, item in enumerate(checklist):
        if not isinstance(item, dict):
            raise ValueError(f"checklist[{i}] が dict ではありません")
        if "category" not in item:
            raise ValueError(f"checklist[{i}] に 'category' がありません")
        cat = item["category"]
        if not isinstance(cat, str) or not cat.strip():
            raise ValueError(f"checklist[{i}].category は非空の文字列である必要があります")
        categories.append(cat)
    return categories


def extract_collector_categories(data: dict) -> list[str]:
    """Collector出力YAMLから collector_output.results[].category を順序保持で抽出"""
    if not isinstance(data, dict):
        raise ValueError("Collector出力YAMLのルートが dict ではありません")
    output = data.get("collector_output")
    if not isinstance(output, dict):
        raise ValueError("Collector出力YAMLに 'collector_output' (dict) がありません")
    results = output.get("results")
    if not isinstance(results, list) or len(results) == 0:
        raise ValueError("collector_output.results が非空 list ではありません")
    categories: list[str] = []
    for i, item in enumerate(results):
        if not isinstance(item, dict):
            raise ValueError(f"collector_output.results[{i}] が dict ではありません")
        if "category" not in item:
            raise ValueError(f"collector_output.results[{i}] に 'category' がありません")
        cat = item["category"]
        if not isinstance(cat, str) or not cat.strip():
            raise ValueError(f"collector_output.results[{i}].category は非空の文字列である必要があります")
        categories.append(cat)
    return categories


def diff_categories(persona_cats: list[str], collector_cats: list[str]) -> dict:
    """2つのカテゴリリストを比較し、欠落・不要・順序差を返す"""
    persona_set = set(persona_cats)
    collector_set = set(collector_cats)
    missing = [c for c in persona_cats if c not in collector_set]
    extra = [c for c in collector_cats if c not in persona_set]
    common = [c for c in persona_cats if c in collector_set]
    # 順序が一致しているか(共通カテゴリ間の相対順)
    collector_common = [c for c in collector_cats if c in persona_set]
    order_mismatch = common != collector_common
    return {
        "missing": missing,
        "extra": extra,
        "order_mismatch": order_mismatch,
    }


def main() -> int:
    if len(sys.argv) < 3:
        print("ERROR: 引数が不足しています", file=sys.stderr)
        print(
            "Usage: python3 check_checklist_completeness.py <persona_yaml_path> <collector_output_yaml_path>",
            file=sys.stderr,
        )
        return 2

    persona_path = sys.argv[1]
    collector_path = sys.argv[2]

    try:
        persona_data = load_yaml(persona_path)
        collector_data = load_yaml(collector_path)
    except Exception as e:
        print(f"ERROR: YAML読み込みに失敗: {e}", file=sys.stderr)
        return 2

    try:
        persona_cats = extract_persona_categories(persona_data)
        collector_cats = extract_collector_categories(collector_data)
    except Exception as e:
        print(f"ERROR: 構造抽出に失敗: {e}", file=sys.stderr)
        return 2

    diff = diff_categories(persona_cats, collector_cats)
    has_issue = bool(diff["missing"] or diff["extra"] or diff["order_mismatch"])

    if not has_issue:
        print(
            f"OK: チェックリスト完全性チェックを通過しました "
            f"(全 {len(persona_cats)} カテゴリ一致、順序OK)"
        )
        return 0

    print(f"FAIL: チェックリスト完全性チェックで不一致を検出しました")
    if diff["missing"]:
        print(f"  欠落カテゴリ ({len(diff['missing'])} 件): Collectorが返さなかった")
        for c in diff["missing"]:
            print(f"    - {c!r}")
    if diff["extra"]:
        print(f"  不要カテゴリ ({len(diff['extra'])} 件): ペルソナに存在しない/誤名の可能性")
        for c in diff["extra"]:
            print(f"    - {c!r}")
    if diff["order_mismatch"]:
        print(f"  順序不一致: ペルソナYAMLとCollector出力でカテゴリ順序が異なります")
        print(f"    ペルソナ: {persona_cats}")
        print(f"    Collector: {collector_cats}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
