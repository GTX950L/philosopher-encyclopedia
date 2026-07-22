#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哲学家百科一致性校验工具（只读，不修改任何文件）。

功能：
  1. 校验哲学家目录中的文件完整性：必须包含所有必需章节。
  2. 校验文档一致性：检测 README / timeline / schools 中
     链接的哲学家是否与目录实际文件匹配。
  3. 检测新添加的哲学家是否已在 mkdocs.yml nav 中注册。

用法：
  python scripts/gen_index.py

返回值：0 = 全部通过，1 = 存在问题。
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
PHIL = os.path.join(CONTENT, "philosophers")

LINK_RE = re.compile(r"philosophers/([\w][\w-]*)\.md")

REQUIRED_SECTIONS = [
    "基本信息",    # 基本信息表格
    "生平时间线",  # 生平时间线
    "核心思想",    # 核心思想
    "代表作品",    # 代表作品
    "对后世的影响",  # 对后世的影响
    "经典名言",    # 经典名言
    "延伸阅读",    # 延伸阅读
]


def collect_entries():
    """扫描 philosophers/ 目录，返回 (filename, display_name) 列表。"""
    files = sorted(glob.glob(os.path.join(PHIL, "*.md")))
    files = [f for f in files if os.path.basename(f) != "index.md"]

    entries = []
    for fpath in files:
        fname = os.path.splitext(os.path.basename(fpath))[0]
        with open(fpath, encoding="utf-8") as f:
            first = f.readline().rstrip("\n")
        m = re.match(r"#\s*(.+?)\s*\(", first)
        disp = m.group(1).strip() if m else fname
        entries.append((fname, disp, fpath))
    return entries


def check_required_sections(entries):
    """检查每篇哲学家条目是否包含必需的章节。"""
    print("\n=== 检查必需章节 ===")
    fail = False
    for fname, disp, fpath in entries:
        with open(fpath, encoding="utf-8") as f:
            text = f.read()
        for section in REQUIRED_SECTIONS:
            if not re.search(rf"^## .*{section}", text, re.MULTILINE):
                print(f"  [FAIL] {fname}.md: 缺少包含「{section}」的章节")
                fail = True
    if not fail:
        print("  [OK] 全部条目包含必需章节")
    return fail


def check_nav_registration(entries):
    """检查所有哲学家是否在 mkdocs.yml nav 中注册。"""
    nav_path = os.path.join(ROOT, "mkdocs.yml")
    if not os.path.exists(nav_path):
        print("  [WARN] mkdocs.yml 不存在，跳过 nav 检查")
        return False

    with open(nav_path, encoding="utf-8") as f:
        nav_text = f.read()

    registered = set(LINK_RE.findall(nav_text))
    actual = {f for f, _, _ in entries}
    missing = actual - registered

    fail = False
    if missing:
        print(f"  [FAIL] 以下哲学家未在 mkdocs.yml nav 中注册：{sorted(missing)}")
        fail = True
    else:
        print("  [OK] 全部哲学家已在 mkdocs.yml nav 中注册")
    return fail


def check_content_consistency(entries):
    """校验各参考文档中哲学家链接与目录的一致性。"""
    print("\n=== 一致性校验 ===")
    names = {f for f, _, _ in entries}
    docs = {
        "README.md": os.path.join(CONTENT, "README.md"),
        "docs/timeline.md": os.path.join(CONTENT, "docs", "timeline.md"),
        "docs/schools.md": os.path.join(CONTENT, "docs", "schools.md"),
    }
    fail = False
    for label, path in docs.items():
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        linked = set(LINK_RE.findall(text))
        missing = names - linked
        orphan = linked - names
        if missing:
            fail = True
            print(f"  [WARN] {label} 缺少 {len(missing)} 位链接：{sorted(missing)}")
        if orphan:
            fail = True
            print(f"  [WARN] {label} 有孤儿链接 {len(orphan)} 个：{sorted(orphan)}")
        if not missing and not orphan:
            print(f"  [OK]   {label} 一致（{len(linked)} 位）")
    if not fail:
        print("  → 全部一致，无漂移。")
    return fail


def main():
    entries = collect_entries()
    total = len(entries)
    print(f"发现 {total} 位哲学家\n")

    has_error = False
    has_error |= check_required_sections(entries)
    has_error |= check_nav_registration(entries)
    has_error |= check_content_consistency(entries)

    print()
    if has_error:
        print("❌ 存在问题，请根据上方提示修复。")
        exit(1)
    else:
        print("✅ 全部校验通过。")


if __name__ == "__main__":
    main()
