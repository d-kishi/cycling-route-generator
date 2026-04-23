#!/usr/bin/env python3
"""
validate_schema.py

ペルソナYAMLがスキーマ（最低限の必須フィールド）を満たしているかを検証する。
新規作成直後のチェックを想定しており、broadlistening_summary は任意。
充実化後のチェックは check_required_fields.py を使う。

Usage:
    python3 validate_schema.py <persona_yaml_path>

Args:
    persona_yaml_path: 検証対象のペルソナYAMLファイルパス

Exit codes:
    0: 検証OK
    1: スキーマ違反あり
    2: 入力エラー（引数不足、ファイル読み込み失敗等）
"""
import sys
import os
import re
import yaml


REQUIRED_TOP_LEVEL = ["id", "name", "description", "attributes", "checklist", "created_at", "last_updated"]
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9\-]*[a-z0-9]$|^[a-z0-9]$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(data: dict) -> list[str]:
    """検証を行い、違反メッセージのリストを返す。空リストならOK。"""
    errors: list[str] = []

    if not isinstance(data, dict):
        return ["YAMLのルートが dict ではありません"]

    for field in REQUIRED_TOP_LEVEL:
        if field not in data:
            errors.append(f"必須フィールド '{field}' が欠けています")

    pid = data.get("id")
    if pid is not None:
        if not isinstance(pid, str) or not pid.strip():
            errors.append("'id' は非空の文字列である必要があります")
        elif not ID_PATTERN.match(pid):
            errors.append(f"'id' は kebab-case 推奨です（a-z, 0-9, ハイフン）: '{pid}'")

    name = data.get("name")
    if name is not None and (not isinstance(name, str) or not name.strip()):
        errors.append("'name' は非空の文字列である必要があります")

    description = data.get("description")
    if description is not None and (not isinstance(description, str) or not description.strip()):
        errors.append("'description' は非空の文字列である必要があります")

    attributes = data.get("attributes")
    if attributes is not None:
        if not isinstance(attributes, dict) or len(attributes) == 0:
            errors.append("'attributes' は最低1項目を持つ dict である必要があります")

    checklist = data.get("checklist")
    if checklist is not None:
        if not isinstance(checklist, list) or len(checklist) == 0:
            errors.append("'checklist' は最低1項目を持つ list である必要があります")
        else:
            for i, item in enumerate(checklist):
                if not isinstance(item, dict):
                    errors.append(f"'checklist[{i}]' は dict である必要があります")
                    continue
                for required_field in ("category", "rationale", "queries"):
                    if required_field not in item:
                        errors.append(f"'checklist[{i}]' に '{required_field}' が欠けています")
                queries = item.get("queries")
                if queries is not None and (not isinstance(queries, list) or len(queries) == 0):
                    errors.append(f"'checklist[{i}].queries' は最低1項目の list である必要があります")

    for date_field in ("created_at", "last_updated"):
        value = data.get(date_field)
        if value is None:
            continue
        # PyYAMLは YYYY-MM-DD を date オブジェクトとしてパースすることがある
        if hasattr(value, "isoformat"):
            continue
        if isinstance(value, str) and DATE_PATTERN.match(value):
            continue
        errors.append(f"'{date_field}' は YYYY-MM-DD 形式である必要があります: {value!r}")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("ERROR: persona_yaml_path が指定されていません", file=sys.stderr)
        print("Usage: python3 validate_schema.py <persona_yaml_path>", file=sys.stderr)
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
        print(f"FAIL: スキーマ違反が {len(errors)} 件見つかりました ({path})")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"OK: スキーマ検証を通過しました ({path})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
