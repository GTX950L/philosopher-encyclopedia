#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按姓名字段生成「拼音索引」页面。
读取 content/philosophers/ 下的 H1 标题（"姓名 (English Name)"），
提取中文姓名并按拼音首字母排序，输出 content/docs/index-by-pinyin.md。

用法：python scripts/gen_pinyin_index.py
"""
import glob, os, re, sys

try:
    from pypinyin import lazy_pinyin, Style
except ImportError:
    sys.stderr.write("缺少依赖：pypinyin。请先 pip install pypinyin\n")
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PHIL = os.path.join(ROOT, "content", "philosophers")
OUT = os.path.join(ROOT, "content", "docs", "index-by-pinyin.md")


def first_letter(cn_name: str) -> str:
    """取中文姓名字符串的首个有效拼音字母。
    跳过非汉字前缀（如希腊字母、西文标点）。"""
    # 移除连字符和点（音译名中间常有"·"或"-"）
    s = cn_name.replace("·", "").replace("-", "").replace(" ", "")
    for ch in s:
        # 仅处理汉字（U+4E00 ~ U+9FFF）
        if "\u4e00" <= ch <= "\u9fff":
            py = lazy_pinyin(ch, style=Style.NORMAL)
            if py and py[0]:
                return py[0][0].upper()
    return "?"


def main():
    files = sorted(glob.glob(os.path.join(PHIL, "*.md")))
    files = [f for f in files if "index.md" not in f]

    items = []
    for fpath in files:
        fname = os.path.splitext(os.path.basename(fpath))[0]
        with open(fpath, encoding="utf-8") as f:
            lines = f.readlines()
        # 跳过 front matter
        i = 0
        if lines and lines[0].strip() == "---":
            for j in range(1, len(lines)):
                if lines[j].strip() == "---":
                    i = j + 1
                    break
        first = lines[i].rstrip("\n") if i < len(lines) else ""
        m = re.match(r"^#\s*(.+?)\s*\((.+)\)\s*$", first)
        if not m:
            continue
        cn_name = m.group(1).strip()
        en_name = m.group(2).strip()
        # 剔除中文名中的全角括号及括号内容（如「王守仁（王阳明）」→「王守仁」）
        cn_clean = re.sub(r"（[^）]*）", "", cn_name).strip()
        if not cn_clean:
            cn_clean = cn_name
        # 英文名过滤掉中文字符（如「Laozi / 道德经」→「Laozi」），并清理多余分隔符
        en_clean = re.sub(r"[\u4e00-\u9fff]+", "", en_name)
        en_clean = re.sub(r"\s*[/|]\s*$", "", en_clean).strip()
        if not en_clean:
            en_clean = en_name
        letter = first_letter(cn_clean)
        # 完整拼音（用于显示）
        full_py = " ".join(lazy_pinyin(cn_clean.replace("·", " ").replace("-", " ")))
        items.append((letter, full_py, cn_clean, en_clean, fname))

    # 排序：按首字母 + 拼音
    items.sort(key=lambda x: (x[0], x[1]))

    lines = [
        "# 🔤 拼音索引",
        "",
        "> 按哲学家**中文姓名首字母**（A-Z）排序的快速检索目录。",
        "> 详细页面请见 [哲学家总览](../philosophers/index.md)。",
        "",
        f"共 **{len(items)} 位**哲学家。",
        "",
        "---",
        "",
        "## 字母索引（A-Z）",
        "",
    ]

    letters = sorted({x[0] for x in items})
    lines.append(" | ".join(f"[{L}](#{L.lower()})" for L in letters))
    lines.append("")
    lines.append("---")
    lines.append("")

    # 分组渲染
    current = None
    counter = 0
    for letter, full_py, cn, en, fname in items:
        if letter != current:
            current = letter
            lines.append(f"## {letter}")
            lines.append("")
            lines.append("| 序号 | 哲学家（中文 / 英文） | 拼音 | 文件 |")
            lines.append("|------|--------------------|------|------|")
        counter += 1
        lines.append(f"| {counter} | {cn} ({en}) | {full_py} | [{fname}.md](../philosophers/{fname}.md) |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 相关导航")
    lines.append("")
    lines.append("- 📖 [哲学家总览（按学习路径）](../philosophers/index.md)")
    lines.append("- 📅 [哲学史时间线（按生卒年）](timeline.md)")
    lines.append("- 🗺️ [哲学流派概览](schools.md)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**最后更新**: 2026年8月  ")
    lines.append("**License**: MIT")

    out = "\n".join(lines) + "\n"
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"已生成 {OUT}，收录 {len(items)} 位哲学家")
    print(f"  首字母分布: {dict(sorted({L: sum(1 for x in items if x[0]==L) for L in letters}.items()))}")


if __name__ == "__main__":
    main()