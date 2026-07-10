#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从哲学家目录自动生成 mkdocs.yml 的 nav 节段。
用法：python scripts/gen_nav.py > nav_patch.yml
然后将输出粘贴到 mkdocs.yml 的 nav: 段落。
"""
import os
import glob
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHIL = os.path.join(ROOT, "philosophers")


def display_name(path):
    """从 H1 提取中文显示名"""
    with open(path, encoding="utf-8") as f:
        first = f.readline().rstrip("\n")
    m = re.match(r"#\s*(.+?)\s*\(", first)
    return m.group(1).strip() if m else os.path.splitext(os.path.basename(path))[0]


def main():
    files = sorted(glob.glob(os.path.join(PHIL, "*.md")))
    files = [f for f in files if os.path.basename(f) != "index.md"]
    print("  - 哲学家:")
    print("      - 总览: philosophers/index.md")
    for fpath in files:
        name = display_name(fpath)
        fname = os.path.basename(fpath)
        print(f"      - {name}: philosophers/{fname}")
    print("  - 参考:")
    print("      - 哲学流派概览: docs/schools.md")
    print("      - 哲学史时间线: docs/timeline.md")
    print("      - 标签分类: tags.md")
    print("      - 条目模板: template.md")
    print("      - 贡献指南: CONTRIBUTING.md")


if __name__ == "__main__":
    main()
