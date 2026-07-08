#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动重建哲学家百科的导航与计数，避免手动维护 34+ 份副本造成漂移。

功能：
  1. 为每个 philosophers/*.md 重建末尾「## 📚 所有哲学家」导航列表
     （按文件名排序，当前页加粗并显示「← 当前页」）。
  2. 同步 README 顶部「已收录-N位」徽章与目录注释中的数字。
  3. 同步 docs/schools.md、docs/timeline.md 顶部的「N位哲学家」计数。

用法：python scripts/gen_index.py
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHIL = os.path.join(ROOT, "philosophers")


def display_name(path):
    """从 H1 提取中文显示名：# 名字 (English) -> 名字"""
    with open(path, encoding="utf-8") as f:
        first = f.readline().rstrip("\n")
    m = re.match(r"#\s*(.+?)\s*\(", first)
    return m.group(1).strip() if m else os.path.splitext(os.path.basename(path))[0]


def main():
    files = sorted(glob.glob(os.path.join(PHIL, "*.md")))
    entries = [(os.path.splitext(os.path.basename(p))[0], display_name(p)) for p in files]
    total = len(entries)
    print(f"发现 {total} 位哲学家")

    # ---- 1) 重建每个条目末尾的导航列表 ----
    head = "## 📚 所有哲学家"
    marker = "⬆️"
    rebuilt = 0
    for fname, disp in entries:
        path = os.path.join(PHIL, fname + ".md")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        if head not in text or marker not in text:
            print(f"  跳过 {fname}（缺少导航区块）")
            continue
        lines = ["", ""]
        for ef, ed in entries:
            if ef == fname:
                lines.append(f"**{ed}** ← 当前页")
            else:
                lines.append(f"- [{ed}]({ef}.md)")
        lines.append("")
        new_block = "\n".join(lines)
        pre, rest = text.split(head, 1)
        before_marker, post = rest.split(marker, 1)
        new_text = pre + head + new_block + marker + post
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
        rebuilt += 1
    print(f"  已重建 {rebuilt} 个导航列表")

    # ---- 2) 同步计数 ----
    readme = os.path.join(ROOT, "README.md")
    t = open(readme, encoding="utf-8").read()
    t = re.sub(r"已收录-\d+位", f"已收录-{total}位", t)
    t = re.sub(r"哲学家条目目录（\d+ 位）", f"哲学家条目目录（{total} 位）", t)
    open(readme, "w", encoding="utf-8").write(t)

    schools = os.path.join(ROOT, "docs", "schools.md")
    t = open(schools, encoding="utf-8").read()
    t = re.sub(r"本项目\d+位哲学家", f"本项目{total}位哲学家", t)
    open(schools, "w", encoding="utf-8").write(t)

    timeline = os.path.join(ROOT, "docs", "timeline.md")
    t = open(timeline, encoding="utf-8").read()
    t = re.sub(r"\d+位哲学家", f"{total}位哲学家", t)
    open(timeline, "w", encoding="utf-8").write(t)

    # ---- 3) 同步 mkdocs.yml ----
    mkdocs = os.path.join(ROOT, "mkdocs.yml")
    t = open(mkdocs, encoding="utf-8").read()
    t = re.sub(r"已收录-\d+位", f"已收录-{total}位", t)
    open(mkdocs, "w", encoding="utf-8").write(t)

    print(f"  计数已同步为 {total}")
    print("DONE")


if __name__ == "__main__":
    main()
