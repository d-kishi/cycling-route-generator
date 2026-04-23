#!/usr/bin/env python3
"""
check_id_uniqueness.py

新規作成しようとしているペルソナのidが、既存の .claude/personas/ 配下の
YAMLと衝突しないかを検証する。

Usage:
    python3 check_id_uniqueness.py <new_id> [personas_dir]

Args:
    new_id: 新規作成予定のペルソナid（例: "weekend-roadie"）
    personas_dir: ペルソナYAMLの格納ディレクトリ（省略時: .claude/personas）

Exit codes:
    0: 重複なし。作成を進めてよい
    1: 重複あり。新規idの変更が必要
    2: 入力エラー（引数不足、ディレクトリ読み込み失敗等）
"""
import sys
import os
import yaml


def main() -> int:
    if len(sys.argv) < 2:
        print("ERROR: new_id が指定されていません", file=sys.stderr)
        print("Usage: python3 check_id_uniqueness.py <new_id> [personas_dir]", file=sys.stderr)
        return 2

    new_id = sys.argv[1].strip()
    if not new_id:
        print("ERROR: new_id が空です", file=sys.stderr)
        return 2

    personas_dir = sys.argv[2] if len(sys.argv) >= 3 else ".claude/personas"

    if not os.path.isdir(personas_dir):
        print(f"INFO: {personas_dir} は存在しません。重複なしとして扱います")
        return 0

    existing_ids = []
    for entry in sorted(os.listdir(personas_dir)):
        if not entry.endswith(".yaml") and not entry.endswith(".yml"):
            continue
        path = os.path.join(personas_dir, entry)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            print(f"WARN: {path} の読み込みに失敗: {e}", file=sys.stderr)
            continue

        if not isinstance(data, dict):
            print(f"WARN: {path} のルートが dict ではありません", file=sys.stderr)
            continue

        pid = data.get("id")
        if pid:
            existing_ids.append((str(pid), entry))

    duplicates = [(pid, fname) for (pid, fname) in existing_ids if pid == new_id]

    if duplicates:
        print(f"FAIL: id '{new_id}' は既に使用されています")
        for pid, fname in duplicates:
            print(f"  - {fname} で使用中")
        print("別の id を指定してください。")
        return 1

    print(f"OK: id '{new_id}' は未使用です（既存 {len(existing_ids)} 件と重複なし）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
