# Claude Skill: Business Analyst（商业分析师）

> 一个面向**决策者**的商业分析师 skill。它的目标不是把数据变漂亮，而是帮决策者做出更好的决定。

## 这个 skill 解决什么问题

大多数 AI 数据分析工具的问题不是不会跑统计，而是：

- 拿到数据立刻开始 `df.describe()`，没人问"这份分析是给谁看的、要支撑什么决策"
- 把"小渠道偶然的高 ROI"当成"应该放量的证据"，不会做小样本警告
- 不区分"当期消耗"和"延迟回款"的时间归因问题，给出错误的 ROI 对比
- 给完建议从不说风险，决策者拿到一个"漂亮的错误答案"

这个 skill 把一套**商业分析师的工作纪律**写成了 prompt：五阶段工作流（前两阶段不许碰数据）、六条分析纪律、三层结论标注、强制风险提示。

## 核心特性

- **五阶段工作流**：业务背景确认 → 商业假设 → 数据探查 → 假设检验 → 报告输出
- **强制业务背景对齐**：在执行任何 `pd.read_*` 之前，必须先确认决策场景和业务机制
- **可被推翻的假设**：分析前提出 2-3 个可被数据证伪的商业假设，避免"先看答案再编题"
- **分析纪律内置**：时间归因检查、小样本警告、边际递减意识、归因公平性、绝对量 vs 比率、反面检验
- **诚实的不确定性标注**：区分【数据直接支撑】/【推断】/【数据不足】三层结论
- **PDF 渲染链路**：Playwright + Paged.js 渲染HTML/CSS为PDF，负责分页、页眉页脚、CJK字体，详见`references/pdf_rendering.md`
- **5套场景报告模板**：`references/templates/`下预置渠道ROI、转化漏斗、留存、AB实验、定价五套模板，视觉风格由执行方按场景判断

## 触发场景

skill 的 description 会在以下场景自动触发：

- 用户提到"数据分析"、"分析数据"、"商业分析"、"策略分析"
- 用户提到"ROI 分析"、"投放效果"、"效率评估"、"优化建议"
- 用户上传 Excel/CSV 并说"帮我看看"、"分析一下这个表"

## 安装

### 方式一：直接 clone 到 skills 目录

```bash
cd ~/.claude/skills
git clone https://github.com/Zuokaiqi/claude-skill-business-analyst business-analyst
```

重启 Claude Code 后，skill 会被自动加载。

### 方式二：作为 Claude Code Plugin 安装

```bash
claude plugin install Zuokaiqi/claude-skill-business-analyst
```

（要求 Claude Code 已启用 plugin 支持）

### 方式三：手动复制

下载本仓库后，将 `skills/business-analyst/` 目录整个复制到 `~/.claude/skills/business-analyst/`。

## 依赖

数据处理的Python环境：

```bash
pip install pandas openpyxl
```

PDF渲染默认走Playwright + Paged.js链路，具体安装步骤和CJK字体要求见`references/pdf_rendering.md`。执行方也可以选用其他渲染工具（weasyprint、reportlab、KIMI/Claude自带PDF能力等），只要能解决A4分页、页眉页脚页码、CJK字体三件事即可。

## 快速开始

安装后，在 Claude Code 中直接说：

> 帮我分析一下 sales_q1.xlsx，老板想看下个季度该把预算压在哪个渠道

skill 会自动触发，并按工作流先反问你 2-3 个业务背景问题（决策场景、业务机制、时间归因等），然后提出商业假设让你确认，再开始读数据。

**不要期待它读完文件就直接出报告**——这是 feature 不是 bug。如果你已经在第一句话里说清了业务背景，它会跳过追问直接进入假设阶段。

## 报告结构

报告结构由阶段一锁定的模板决定。5套模板（渠道ROI、转化漏斗、留存、AB实验、定价）都包含公共锚点章节：商业假设、Actionable Insight、分析局限性、References；场景特有章节和推荐指标由模板文件自己定义，具体参见`references/templates/`。

## 与"普通数据分析 prompt"的差别

| 维度 | 普通分析 | 本 skill |
|---|---|---|
| 起手式 | 立刻 `df.read_excel` | 先问决策场景和业务机制 |
| 假设 | 没有 / 描述性统计 | 2-3 个可被数据推翻的具体假设 |
| 小样本 | 直接给比率和建议 | 强制 **【小样本】** 标注 + 拒绝放量建议 |
| 时间归因 | 当期消耗 ÷ 当期回款 = ROI | 强制提示时间错位风险 |
| 风险提示 | 几乎没有 | 每个建议都附 **反面检验** 和熔断线 |
| 结论态度 | 结论确定 | 区分【数据直接支撑】/【推断】/【数据不足】 |

## 文件结构

```
business-analyst/
├── SKILL.md                       # 主 prompt（角色 + 工作流 + 阶段一模板选择）
├── references/
│   ├── pdf_rendering.md          # PDF 渲染技术路径（Playwright + Paged.js）
│   ├── report_examples.md        # 好/差分析对比示例
│   └── templates/                # 5 套报告模板
│       ├── channel_roi.md
│       ├── funnel_conversion.md
│       ├── retention.md
│       ├── ab_test.md
│       └── pricing.md
└── scripts/                       # 历史辅助脚本，非默认执行路径
    ├── chart_style.py
    └── pdf_report.py
```

## 给其他 Agent 使用

如果你想把这个 skill 用在 **非 Claude 体系**的 Agent 上（Kimi、GPT、自建 LangChain 等），将 `SKILL.md` + `references/*.md` + `references/templates/*.md` 拼接成一个完整的 system prompt 喂给目标模型即可。该 skill 的价值在 prompt 而非代码，几乎不依赖 Claude harness 的特殊机制。

## License

MIT

## 致谢

工作流设计受到经典的"分析师工作纪律"影响，把那些资深分析师才会注意的陷阱（时间归因、小样本陷阱、边际递减、归因偏差）显式写进 prompt，让 AI 也能避开。
