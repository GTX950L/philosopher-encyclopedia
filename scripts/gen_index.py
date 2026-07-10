#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动重建哲学家百科的导航与计数，并校验索引一致性，避免手动维护造成漂移。

功能：
  1. 为每个 philosophers/*.md 重建末尾「## 📚 所有哲学家」导航列表
     （按文件名排序，当前页加粗并显示「← 当前页」）。
  2. 同步 README / docs/schools.md / docs/timeline.md / mkdocs.yml 顶部
     「已收录-N位」计数。
  3. 一致性校验：比对 philosophers/ 实际文件与 README / timeline / schools
     中出现的哲学家链接，发现遗漏或孤儿链接时打印警告（不阻断，便于增量修复）。

用法：python scripts/gen_index.py
"""
import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
PHIL = os.path.join(CONTENT, "philosophers")

# 匹配 [显示名](philosophers/xxx.md) 中的文件名（注意：links以philosophers/开头，实际文件在content/philosophers/）
LINK_RE = re.compile(r"philosophers/([\w][\w-]*)\.md")


def display_name(path):
    """从 H1 提取中文显示名：# 名字 (English) -> 名字"""
    with open(path, encoding="utf-8") as f:
        first = f.readline().rstrip("\n")
    m = re.match(r"#\s*(.+?)\s*\(", first)
    return m.group(1).strip() if m else os.path.splitext(os.path.basename(path))[0]


def check_consistency(entries):
    """校验文档中哲学家链接与目录文件的一致性，打印差异。"""
    names = {f for f, _ in entries}
    docs = {
        "README.md": os.path.join(CONTENT, "README.md"),
        "docs/timeline.md": os.path.join(CONTENT, "docs", "timeline.md"),
        "docs/schools.md": os.path.join(CONTENT, "docs", "schools.md"),
    }
    print("\n=== 一致性校验 ===")
    all_ok = True
    for label, path in docs.items():
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8").read()
        linked = set(LINK_RE.findall(text))
        missing = names - linked            # 在目录但文档未链接（漏人）
        orphan = linked - names             # 文档链接了但目录无文件（断链）
        if missing:
            all_ok = False
            print(f"  [WARN] {label} 缺少 {len(missing)} 位：{sorted(missing)}")
        if orphan:
            all_ok = False
            print(f"  [WARN] {label} 有孤儿链接 {len(orphan)} 个：{sorted(orphan)}")
        if not missing and not orphan:
            print(f"  [OK]   {label} 一致（{len(linked)} 位）")
    if all_ok:
        print("  → 全部一致，无漂移。")
    else:
        print("  → 存在漂移，请按上方提示补全名单（数字已自动同步，名单需手动）。")
    return all_ok


def main():
    files = sorted(glob.glob(os.path.join(PHIL, "*.md")))
    # 排除目录索引页，避免把 index.md 当作哲学家条目
    files = [f for f in files if os.path.basename(f) != "index.md"]
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
    readme = os.path.join(CONTENT, "README.md")
    t = open(readme, encoding="utf-8").read()
    t = re.sub(r"已收录-\d+位", f"已收录-{total}位", t)
    t = re.sub(r"哲学家条目目录（\d+ 位）", f"哲学家条目目录（{total} 位）", t)
    open(readme, "w", encoding="utf-8").write(t)

    schools = os.path.join(CONTENT, "docs", "schools.md")
    t = open(schools, encoding="utf-8").read()
    t = re.sub(r"本项目\d+位哲学家", f"本项目{total}位哲学家", t)
    open(schools, "w", encoding="utf-8").write(t)

    timeline = os.path.join(CONTENT, "docs", "timeline.md")
    t = open(timeline, encoding="utf-8").read()
    t = re.sub(r"\d+位哲学家", f"{total}位哲学家", t)
    open(timeline, "w", encoding="utf-8").write(t)

    mkdocs = os.path.join(ROOT, "mkdocs.yml")
    if os.path.exists(mkdocs):
        t = open(mkdocs, encoding="utf-8").read()
        t = re.sub(r"已收录-\d+位", f"已收录-{total}位", t)
        open(mkdocs, "w", encoding="utf-8").write(t)

    print(f"  计数已同步为 {total}")

    # ---- 3) 一致性校验 ----
    check_consistency(entries)

    print("DONE")


if __name__ == "__main__":
    main()
