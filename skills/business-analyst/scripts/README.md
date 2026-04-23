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

版式和配色规范统一参考`../references/report_style.md`，不论使用哪种工具，输出效果应与规范保持一致。
