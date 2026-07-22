# 更新日志 (Changelog)

## [2.0.0] - 2026-07-22

### 🚀 重大变更：从 MkDocs 迁移至 Zensical

本项目从 MkDocs + Material for MkDocs 迁移至 [Zensical](https://zensical.org) —— 由 Material for MkDocs 原班团队打造的下一代静态站点生成器。

#### 变更内容
- **`mkdocs.yml`**：移除暂不支持的插件（git-revision-date-localized、minify、tags、redirects），Zensical 原生读取该配置
- **`requirements.txt`**：`mkdocs-material` → `zensical`
- **`.github/workflows/deploy-pages.yml`**：`mkdocs build` → `zensical build`
- **`.github/workflows/validate-entries.yml`**：去除多余依赖安装步骤
- **`CONTRIBUTING.md`**：`mkdocs serve` → `zensical serve`

#### 已知限制（Zensical 仍处于 alpha 阶段）
- 页面底部不显示"最后更新日期"（git-revision-date-localized 暂未实现）
- tags.md 标签分类页暂不自动聚合（tags 插件暂未实现）
- HTML 不自动压缩（minify 插件暂未实现）

---

## [1.0.1] - 2026-07-10

### 新增
- 添加 `requirements.txt`：本地开发依赖一键安装 (#2)
- 添加 `CHANGELOG.md`：项目更新日志 (#3)
- 添加 `.editorconfig`：统一多编辑器格式配置 (#4)
- 添加 `.github/dependabot.yml`：自动检查依赖更新 (#5)
- 添加 GitHub Actions 构建状态徽章到 README (#6)
- 在 CONTRIBUTING.md 中补充本地开发环境指南 (#7)

### 优化
- 更新 `validate-entries.yml`：PR 时自动运行 `gen_index.py` 验证一致性 (#8)
- 更新 `mkdocs.yml`：启用 tags 插件，按流派/时代/地域标签分类 (#9)
- 更新 `_config.yml`：增加 MkDocs 与 Jekyll 协同说明 (#10)
- 在 README 中说明 Jekyll/MkDocs 双配置文件的关系 (#11)

### 基础设施
- 配置 Dependabot 每周扫描 GitHub Actions 和 pip 依赖 (#12)

---

## [1.0.0] - 2026-06-13

### 初始发布
- 首批收录 42 位哲学家条目
- 五阶学习路径 README
- 哲学流派概览 (`docs/schools.md`)
- 哲学史时间线 (`docs/timeline.md`)
- MkDocs Material 文档站点 + GitHub Pages 部署
- CI 工作流：条目验证、链接检查、自动部署
- 贡献指南 (CONTRIBUTING.md)
- 条目模板 (template.md)
- Issue Template：报告错误、改进建议、新哲学家申请
