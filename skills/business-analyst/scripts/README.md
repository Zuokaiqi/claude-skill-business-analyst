# scripts 目录说明

本目录是**本机可选的历史辅助脚本**，不属于skill的默认执行路径。

- `chart_style.py`：6套配色主题的matplotlib样式封装
- `pdf_report.py`：基于fpdf2的PDF渲染封装

## SKILL.md 默认流程不依赖这些脚本

阶段五的PDF生成由执行方自行选择工具完成。只有当执行环境已安装`fpdf2 >= 2.7`且系统中有可用中文字体（如微软雅黑、Noto Sans CJK、思源黑体）时，这两个脚本才能作为参考使用。

## 其他环境应使用各自的 PDF 能力

- Claude Code：优先使用`anthropic-skills:pdf`等内置PDF skill
- KIMI：使用自带的PDF生成能力
- 通用Python环境：reportlab、weasyprint、matplotlib+PIL拼图等方案都可以

视觉规范已从skill中移除，视觉由执行方按场景自行决定。默认PDF渲染链路见`../references/pdf_rendering.md`，报告结构模板见`../references/templates/`。

`chart_style.py`的6套主题常量无外部文档依赖，仅作为需要matplotlib配色起点的执行方的参考代码。`pdf_report.py`同样是fpdf2时代的历史封装。两者均不参与v3默认渲染链路，不维护、不保证向前兼容。
