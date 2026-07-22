# 贡献指南 (Contributing Guide)

感谢你对哲学家百科全书项目的关注！我们欢迎任何形式的贡献。

参与本项目即表示你同意遵守我们的 [行为准则](CODE_OF_CONDUCT.md)（Contributor Covenant v2.1）。

---

## 🚀 本地开发环境搭建

### 前置要求
- Python 3.9+
- Git

### 步骤

```bash
# 1. Fork 本仓库
# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/philosopher-encyclopedia.git
cd philosopher-encyclopedia

# 3. 安装依赖
pip install -r requirements.txt

# 4. 本地预览站点
zensical serve
# 访问 http://127.0.0.1:8000 查看效果

# 5. （可选）运行一致性校验
python scripts/gen_index.py

# 6. 创建新分支并提交
git checkout -b my-change
git add .
git commit -m "描述你的更改"
git push origin my-change

# 7. 在 GitHub 上创建 Pull Request
```

### 目录结构说明

```
philosopher-encyclopedia/
├── requirements.txt        # Python 依赖（pip install -r）
├── mkdocs.yml              # Zensical 站点配置（兼容 MkDocs 格式）
├── philosophers/           # 哲学家条目（核心内容）
│   ├── index.md            # 总览索引
│   ├── camus.md            # 示例条目
│   └── ...
├── docs/                   # 补充文档
│   ├── schools.md          # 流派概览
│   └── timeline.md         # 时间线
├── scripts/
│   └── gen_index.py        # 一致性校验（只读，不改文件）
└── template.md             # 新条目模板
```

---

## 🎯 如何贡献

### 1. 添加新哲学家条目

**步骤**：
1. Fork 本仓库
2. 在 `philosophers/` 目录下创建新的 Markdown 文件（文件名用英文名，如 `plato.md`）
3. 使用 `template.md` 作为模板
4. 运行 `python scripts/gen_index.py` 校验一致性（只读检查，不需要预提交）
5. 提交 Pull Request

**要求**：
- 条目需包含：生平、核心思想、代表作品、历史影响四个基本部分
- 引用的观点需注明来源
- 保持客观中立的学术态度
- 中文写作，语言流畅易懂

### 2. 完善现有条目

如果发现现有条目有：
- 事实错误
- 遗漏重要信息
- 表述不清
- 缺少参考资料

欢迎提交 Issue 或 Pull Request 进行修正。

### 3. 改进项目结构

- 提出新的分类方式
- 添加索引或导航
- 优化 README 或文档

---

## 📝 条目写作规范

### 文件命名
- 使用英文小写字母
- 多个单词用连字符连接
- 示例：`friedrich-nietzsche.md`, `confucius.md`

### 内容结构
请参考 `template.md`，包含以下部分：
1. 基本信息表格
2. 生平时间线
3. 核心思想
4. 代表作品
5. 对后世的影响
6. 经典名言
7. 延伸阅读

### 引用规范
- 直接引用需注明出处（著作名称 + 页码）
- 推荐书籍需注明作者、译者、出版社
- 在线资源需提供可访问的链接

### 语言风格
- 使用现代汉语，避免过于学术化的术语（或提供解释）
- 保持客观，避免主观评价
- 尊重不同哲学观点，不贬低任何流派

---

## 🚀 提交流程

### 方式一：GitHub Web 界面（推荐新手）
1. 点击文件右上角的铅笔图标进行编辑
2. 修改完成后点击 "Commit changes"
3. 提交 Pull Request

### 方式二：本地开发（推荐熟练用户）
```bash
# 1. Fork 本仓库
# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/philosopher-encyclopedia.git
cd philosopher-encyclopedia

# 3. 创建新分支
git checkout -b add-new-philosopher

# 4. 添加或修改文件
# ... 编辑文件 ...

# 5. （可选）运行一致性校验
python scripts/gen_index.py

# 6. 提交更改
git add .
git commit -m "添加 XXX 哲学家条目"

# 7. 推送到你的 Fork
git push origin add-new-philosopher

# 8. 在 GitHub 上创建 Pull Request
```

---

## 💡 选题建议

### 优先添加的哲学家
- **古希腊**: 苏格拉底、柏拉图、亚里士多德、赫拉克利特
- **中国**: 孔子、老子、庄子、墨子
- **欧洲近代**: 笛卡尔、斯宾诺莎、莱布尼茨、洛克、休谟
- **德国古典**: 康德、费希特、谢林、黑格尔
- **19世纪**: 叔本华、马克思、密尔、克尔凯郭尔
- **20世纪**: 胡塞尔、海德格尔、维特根斯坦、波普尔、福柯

### 待补充的哲学流派
以下重要流派目前尚未收录代表性人物，欢迎贡献：

| 流派 | 推荐人物 | 参考资料 |
|------|---------|---------|
| 中世纪哲学 | 奥古斯丁、托马斯·阿奎那 | 经院哲学奠基人 |
| 文艺复兴 | 马基雅维利、蒙田 | 政治哲学与怀疑论 |
| 中国宋明理学 | 朱熹、王阳明 | 理学与心学集大成者 |
| 法兰克福学派 | 哈贝马斯 | 交往行为理论 |
| 实用主义 | 威廉·詹姆斯、皮尔士 | 实用主义三杰缺二 |

### 选择标准
- 对哲学史有重大影响
- 思想具有现实意义
- 有可靠的参考资料

---

## ❓ 常见问题

**Q: 我对哲学不太了解，可以贡献吗？**  
A: 当然可以！你可以：
- 修正错别字或格式问题
- 添加参考资料链接
- 翻译外文资料
- 提出改进建议

**Q: 如何避免事实错误？**  
A: 
- 参考多部权威著作
- 查阅学术资料（斯坦福哲学百科、互联网哲学百科等）
- 在提交前请他人审阅

**Q: 可以添加当代哲学家吗？**  
A: 可以，但需满足：
- 对哲学领域有公认的重大贡献
- 有代表性的著作
- 思想已经过一定时间的检验

**Q: 提交前必须运行 gen_index.py 吗？**  
A: CI 中的 validate-entries.yml 会自动运行 `python scripts/gen_index.py` 做一致性校验，检查必需章节是否齐全、新添加的哲学家是否在 mkdocs.yml 中注册等。脚本是**只读的**，不会修改任何文件，放心运行。

---

## 📧 联系方式

如有疑问，欢迎：
- 提交 [Issue](https://github.com/GTX950L/philosopher-encyclopedia/issues)
- 邮件联系：GTX950L（通过 GitHub 个人主页获取）

---

**再次感谢你的贡献！** 🙏
