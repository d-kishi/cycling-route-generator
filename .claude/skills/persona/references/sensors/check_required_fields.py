#!/usr/bin/env python3
"""
check_required_fields.py

ブロードリスニング充実化後のペルソナYAMLが、必須フィールド（broadlistening_summary含む）を
満たしているかを検証する。validate_schema.py より厳しく、中身の構造まで見る。

Usage:
    python3 check_required_fields.py <persona_yaml_path>

Args:
    persona_yaml_path: 検証対象のペルソナYAMLファイルパス

Exit codes:
    0: 検証OK
    1: 必須フィールド不足あり
    2: 入力エラー
"""
import sys
import os
import yaml


ALLOWED_SOURCE_TYPES = {"primary", "community", "sns", "blog"}
ALLOWED_LEVELS = {"high", "medium", "low"}


def validate_summary_entry(entry: dict, idx: int) -> list[str]:
    errors: list[str] = []

    if not isinstance(entry, dict):
        return [f"'broadlistening_summary[{idx}]' は dict である必要があります"]

    for field in ("category", "summary", "sources", "self_assessment"):
        if field not in entry:
            errors.append(f"'broadlistening_summary[{idx}]' に '{field}' が欠けています")

    category = entry.get("category")
    if category is not None and (not isinstance(category, str) or not category.strip()):
        errors.append(f"'broadlistening_summary[{idx}].category' は非空の文字列である必要があります")

    summary = entry.get("summary")
    if summary is not None and (not isinstance(summary, str) or not summary.strip()):
        errors.append(f"'broadlistening_summary[{idx}].summary' は非空の文字列である必要があります")

    sources = entry.get("sources")
    if sources is not None:
        if not isinstance(sources, list) or len(sources) == 0:
            errors.append(f"'broadlistening_summary[{idx}].sources' は最低1項目の list である必要があります")
        else:
            for j, src in enumerate(sources):
                if not isinstance(src, dict):
                    errors.append(f"'broadlistening_summary[{idx}].sources[{j}]' は dict である必要があります")
                    continue
                if "url" not in src or not isinstance(src.get("url"), str) or not src["url"].strip():
                    errors.append(f"'broadlistening_summary[{idx}].sources[{j}].url' が未設定または不正です")
                src_type = src.get("type")
                if src_type is None:
                    errors.append(f"'broadlistening_summary[{idx}].sources[{j}].type' が未設定です")
                elif src_type not in ALLOWED_SOURCE_TYPES:
                    errors.append(
                        f"'broadlistening_summary[{idx}].sources[{j}].type' は {sorted(ALLOWED_SOURCE_TYPES)} のいずれか: {src_type!r}"
                    )

    self_assessment = entry.get("self_assessment")
    if self_assessment is not None:
        if not isinstance(self_assessment, dict):
            errors.append(f"'broadlistening_summary[{idx}].self_assessment' は dict である必要があります")
        else:
            for level_field in ("coverage", "confidence"):
                value = self_assessment.get(level_field)
                if value is None:
                    errors.append(f"'broadlistening_summary[{idx}].self_assessment.{level_field}' が未設定です")
                elif value not in ALLOWED_LEVELS:
                    errors.append(
                        f"'broadlistening_summary[{idx}].self_assessment.{level_field}' は {sorted(ALLOWED_LEVELS)} のいずれか: {value!r}"
                    )

    return errors


def validate(data: dict) -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["YAMLのルートが dict ではありません"]

    if "broadlistening_summary" not in data:
        errors.append("必須フィールド 'broadlistening_summary' が欠けています（充実化未完了の可能性）")
        return errors

    bs = data["broadlistening_summary"]
    if not isinstance(bs, list) or len(bs) == 0:
        errors.append("'broadlistening_summary' は最低1項目の list である必要があります")
        return errors

    checklist = data.get("checklist", [])
    checklist_categories: list[str] = []
    if isinstance(checklist, list):
        for item in checklist:
            if isinstance(item, dict) and isinstance(item.get("category"), str):
                checklist_categories.append(item["category"])

    summary_categories: list[str] = []
    for i, entry in enumerate(bs):
        errors.extend(validate_summary_entry(entry, i))
        if isinstance(entry, dict) and isinstance(entry.get("category"), str):
            summary_categories.append(entry["category"])

    if checklist_categories:
        missing = [c for c in checklist_categories if c not in summary_categories]
        if missing:
            errors.append(
                f"checklist にある次のカテゴリが broadlistening_summary に存在しません: {missing}"
            )

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("ERROR: persona_yaml_path が指定されていません", file=sys.stderr)
        print("Usage: python3 check_required_fields.py <persona_yaml_path>", file=sys.stderr)
        return 2

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f"ERROR: ファイルが見つかりません: {path}", file=sys.stderr)
        return 2

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        print(f"ERROR: YAML読み込みに失敗: {e}", file=sys.stderr)
        return 2

    errors = validate(data)
    if errors:
        print(f"FAIL: 必須フィールド不足が {len(errors)} 件見つかりました ({path})")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK: 充実化後の必須フィールド検証を通過しました ({path})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
