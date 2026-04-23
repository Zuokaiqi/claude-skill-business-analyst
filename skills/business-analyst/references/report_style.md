# PDF 报告样式规范

## 整体风格

深色主题，参考数据仪表盘风格。默认使用midnight主题，色值示例如下，完整6套主题见下面的「主题色值清单」：
- 页面背景：深蓝黑 (#1A1A2E)
- 卡片背景：深灰蓝 (#23284A)
- 正文字色：浅灰白 (#BEC3D7)
- 标题字色：纯白 (#FFFFFF)
- 主色调：粉色 (#E91E8C) 和蓝色 (#4A9EF5)

## 主题色值清单

本skill提供6套配色主题，执行方按场景选用。每套主题给出11个核心色值字段：`page_bg`（页面底色）、`surface_bg`（卡片/容器底色）、`text`（正文字色）、`title`（标题字色）、`grid`（网格线/分隔线）、`primary`（主色，强调/高亮）、`secondary`（辅色，对比/次级强调）、`accent`（点缀色，警示/数据不足）、`success`（成功/假设成立）、`danger`（失败/假设推翻）、`purple`（紫色调，用于第4条及以上的序列色）。

### midnight（默认，深蓝紫暗色）

| 字段 | 色值 |
|------|------|
| page_bg | #1A1A2E |
| surface_bg | #23284A |
| text | #BEC3D7 |
| title | #FFFFFF |
| grid | #363758 |
| primary | #E91E8C |
| secondary | #4A9EF5 |
| accent | #F5A623 |
| success | #2ECC71 |
| danger | #E74C3C |
| purple | #7B68EE |

### ocean（深海蓝）

| 字段 | 色值 |
|------|------|
| page_bg | #0B1929 |
| surface_bg | #132F4C |
| text | #B0C4DE |
| title | #E8F4FD |
| grid | #1E3F60 |
| primary | #3B82F6 |
| secondary | #22D3EE |
| accent | #F59E0B |
| success | #06D6A0 |
| danger | #EF4444 |
| purple | #818CF8 |

### forest（深绿色）

| 字段 | 色值 |
|------|------|
| page_bg | #0A1A14 |
| surface_bg | #12302A |
| text | #A7C4B5 |
| title | #E8F5EE |
| grid | #1A4035 |
| primary | #10B981 |
| secondary | #34D399 |
| accent | #F97316 |
| success | #4ADE80 |
| danger | #FB7185 |
| purple | #A78BFA |

### ember（暖棕色）

| 字段 | 色值 |
|------|------|
| page_bg | #1A1008 |
| surface_bg | #2D1F10 |
| text | #D4B896 |
| title | #FFF8EE |
| grid | #4A3018 |
| primary | #F59E0B |
| secondary | #FBBF24 |
| accent | #8B5CF6 |
| success | #86EFAC |
| danger | #FCA5A5 |
| purple | #C084FC |

### lavender（深紫色）

| 字段 | 色值 |
|------|------|
| page_bg | #13101F |
| surface_bg | #1E1A32 |
| text | #C4B8E8 |
| title | #F0ECFF |
| grid | #2E2850 |
| primary | #A78BFA |
| secondary | #C4B5FD |
| accent | #06B6D4 |
| success | #6EE7B7 |
| danger | #F9A8D4 |
| purple | #E879F9 |

### minimal（浅色白底）

| 字段 | 色值 |
|------|------|
| page_bg | #FFFFFF |
| surface_bg | #F8FAFC |
| text | #475569 |
| title | #1E293B |
| grid | #E2E8F0 |
| primary | #2563EB |
| secondary | #3B82F6 |
| accent | #F97316 |
| success | #16A34A |
| danger | #DC2626 |
| purple | #7C3AED |

## 组件规范

### 封面
- 粉色大色块头部
- 报告标题（28pt 加粗，白色）
- 副标题（12pt，时间范围 + 分析目的）
- 核心指标卡片（2x2 布局）

### 标题
- 一级标题：白色 16pt 加粗，左侧粉色竖条（3px 宽）
- 二级标题：灰色 10pt，用于假设验证标签等辅助信息

### 假设验证标签
- 深紫背景小标签，橙色文字
- 格式："验证假设 X：[假设内容简述]"

### 结论高亮
- 假设成立：绿色 (#2ECC71) 加粗文字
- 假设被推翻：红色 (#E74C3C) 加粗文字
- 数据不足以判断：橙色 (#F5A623) 加粗文字

### 建议动作框
- 深紫背景 + 粉色左边框
- 粉色文字，与正文明确区分

### 表格
- 表头：深蓝灰背景 (#363758)，灰白文字
- 数据行：深浅交替（#1E233A / #1A1E32）
- ROI/关键指标列：>1 绿色，<1 红色
- 第一列（名称列）加粗

### Key Metrics 卡片
- 2x2 网格布局
- 指标名：小号灰色
- 指标值：大号粉色加粗
- 说明：小号灰色

### 图表容器
- 深色边框包裹
- 底部居中小号灰色图注

### 页脚
- 报告名称 + 页码，居中，小号灰色

## 字体与渲染要求

- 中文字体：优先微软雅黑（msyh.ttc / msyhbd.ttc）、Noto Sans CJK、思源黑体等完整覆盖CJK的字体。字体缺失会导致PDF全页乱码，执行前必须确认
- 粗体字体：优先使用同字族的粗体（如msyhbd.ttc），备选与常规字体相同
- PDF工具执行方自选：fpdf2、reportlab、weasyprint、puppeteer/playwright截图，或执行方自带的PDF skill都可以
- DPI：150
- 分页：每个分析维度独立分页

## 风险/局限性标注样式

报告中涉及不确定性的内容，用以下视觉方式标注：
- **【小样本】**：橙色文字标签
- **【推断】**：橙色文字标签
- **【数据不足】**：红色文字标签
- **【未做时间归因校正】**：橙色文字标签

这些标注不是可有可无的装饰，是分析纪律的一部分。