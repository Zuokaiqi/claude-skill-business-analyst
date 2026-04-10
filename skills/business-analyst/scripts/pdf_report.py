"""
数据分析技能 - PDF 报告生成器

把 references/report_style.md 的样式规范固化为可调用的 API，
避免每次会话都要重新发明 fpdf2 的中文字体注册、卡片布局、表格交替色等。

依赖: fpdf2 (>=2.7), pillow

标准用法：

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / '.claude' / 'skills' / 'business-analyst' / 'scripts'))
    from pdf_report import Report

    r = Report(title='2026 Q1 渠道 ROI 分析', subtitle='2026-01-01 ~ 2026-03-31')
    r.add_cover(metrics=[
        ('总消耗', '¥234万', '同比 +12%'),
        ('总回款', '¥1,180万', '同比 +28%'),
        ('整体 ROI', '5.04', '行业均值 3.2'),
        ('签约客户', '342', '单客成本 ¥6,842'),
    ])

    r.new_section()
    r.add_h1('维度一：渠道效率对比')
    r.add_hypothesis_label(1, '小红书 ROI 显著优于抖音信息流')
    r.add_text('小红书消耗 21 万，回款 84 万，简单 ROI 3.95...')
    r.add_warning('【未做时间归因校正】 加盟周期 1-3 个月', level='warn')
    r.add_chart('chart_channel_roi.png', caption='图1 各渠道 ROI 对比')
    r.add_table(
        headers=['渠道', '消耗(万)', '回款(万)', 'ROI', '签约数'],
        rows=[
            ['小红书', '21.0', '83.0', '3.95', '61'],
            ['抖音信息流', '156.0', '79.6', '0.51', '142'],
        ],
        roi_col=3,
    )
    r.add_conclusion('假设成立：小红书当期 ROI 显著高于抖音', status='hold')
    r.add_action('建议小红书预算从 21 万增至 40 万 (+90%)，设置 ROI<2.0 熔断线。')

    r.save('report.pdf')
"""
import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# 自举：把本文件所在目录加入 sys.path，使 chart_style 无论调用方是否
# 提前 sys.path.insert 都能被解析到（同目录两个模块互相依赖）。
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from chart_style import find_chinese_font_path

# ─────────────────────────────────────────────
# 颜色（与 references/report_style.md 严格对应，RGB 元组）
# ─────────────────────────────────────────────
BG_PAGE = (26, 26, 46)          # #1A1A2E
BG_CARD = (35, 40, 74)          # #23284A
BG_TABLE_HEADER = (54, 55, 88)  # #363758
BG_TABLE_ROW_A = (30, 35, 58)   # #1E233A
BG_TABLE_ROW_B = (26, 30, 50)   # #1A1E32
BG_PURPLE = (47, 35, 78)        # 深紫，用于建议框 / 假设标签

TEXT_BODY = (190, 195, 215)     # #BEC3D7
TEXT_TITLE = (255, 255, 255)    # #FFFFFF
TEXT_MUTED = (140, 145, 170)

PINK = (233, 30, 140)           # #E91E8C
BLUE = (74, 158, 245)           # #4A9EF5
ORANGE = (245, 166, 35)         # #F5A623
GREEN = (46, 204, 113)          # #2ECC71
RED = (231, 76, 60)             # #E74C3C


class Report(FPDF):
    """商业数据分析 PDF 报告"""

    def __init__(self, title='数据分析报告', subtitle=''):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.report_title = title
        self.report_subtitle = subtitle
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(15, 15, 15)

        regular = find_chinese_font_path(bold=False)
        if not regular:
            raise FileNotFoundError(
                '未找到中文字体。请安装微软雅黑 / 思源黑体 / 文泉驿微米黑后重试。'
            )
        bold = find_chinese_font_path(bold=True) or regular
        self.add_font('CN', '', regular)
        self.add_font('CN', 'B', bold)
        self.set_font('CN', '', 11)

    # ─── 页面装饰 ───────────────────────────

    def header(self):
        # 整页深色背景
        self.set_fill_color(*BG_PAGE)
        self.rect(0, 0, self.w, self.h, 'F')
        # 重置光标到顶部边距
        self.set_xy(self.l_margin, self.t_margin)

    def footer(self):
        self.set_y(-12)
        self.set_font('CN', '', 8)
        self.set_text_color(*TEXT_MUTED)
        self.cell(0, 6, f'{self.report_title}    -  {self.page_no()}  -', align='C')

    # ─── 封面 ───────────────────────────────

    def add_cover(self, metrics=None):
        """
        封面页。
        metrics: 最多 4 个 (名称, 数值, 说明) 元组，2x2 网格展示。
        """
        self.add_page()
        # 粉色头部色块
        self.set_fill_color(*PINK)
        self.rect(0, 0, self.w, 70, 'F')
        # 标题
        self.set_xy(15, 22)
        self.set_text_color(*TEXT_TITLE)
        self.set_font('CN', 'B', 24)
        self.cell(0, 14, self.report_title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        # 副标题
        if self.report_subtitle:
            self.set_x(15)
            self.set_font('CN', '', 12)
            self.cell(0, 8, self.report_subtitle)
        # 关键指标卡片
        if metrics:
            self.set_y(90)
            self._draw_metric_grid(metrics)

    def _draw_metric_grid(self, metrics):
        """2x2 关键指标卡片，最多 4 个"""
        metrics = list(metrics)[:4]
        card_w = (self.w - 30 - 6) / 2
        card_h = 36
        x0, y0 = 15, self.get_y()
        for i, item in enumerate(metrics):
            name, value, desc = (list(item) + ['', ''])[:3]
            row, col = divmod(i, 2)
            x = x0 + col * (card_w + 6)
            y = y0 + row * (card_h + 6)
            self.set_fill_color(*BG_CARD)
            self.rect(x, y, card_w, card_h, 'F')
            self.set_xy(x + 5, y + 5)
            self.set_text_color(*TEXT_MUTED)
            self.set_font('CN', '', 9)
            self.cell(card_w - 10, 5, str(name))
            self.set_xy(x + 5, y + 12)
            self.set_text_color(*PINK)
            self.set_font('CN', 'B', 20)
            self.cell(card_w - 10, 11, str(value))
            self.set_xy(x + 5, y + 25)
            self.set_text_color(*TEXT_MUTED)
            self.set_font('CN', '', 8)
            self.cell(card_w - 10, 5, str(desc))
        self.set_y(y0 + 2 * (card_h + 6) + 6)

    def add_metric_cards(self, metrics):
        """正文中插入 Key Metrics 卡片（2x2，最多 4 个）"""
        self.ln(4)
        self._draw_metric_grid(metrics)

    # ─── 章节与标题 ─────────────────────────

    def new_section(self):
        """每个分析维度独立分页"""
        self.add_page()

    def add_h1(self, text):
        """一级标题：白色 14pt 加粗，左侧粉色竖条"""
        self.ln(3)
        y = self.get_y()
        self.set_fill_color(*PINK)
        self.rect(15, y + 2, 1.4, 9, 'F')
        self.set_xy(18, y)
        self.set_text_color(*TEXT_TITLE)
        self.set_font('CN', 'B', 15)
        self.cell(0, 12, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def add_h2(self, text):
        self.ln(2)
        self.set_text_color(*TEXT_TITLE)
        self.set_font('CN', 'B', 12)
        self.cell(0, 8, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def add_hypothesis_label(self, idx, summary):
        """假设验证标签：深紫背景 + 橙色文字"""
        self.ln(1)
        text = f'  验证假设 {idx}：{summary}  '
        self.set_fill_color(*BG_PURPLE)
        self.set_text_color(*ORANGE)
        self.set_font('CN', '', 9)
        w = self.get_string_width(text) + 4
        self.cell(w, 7, text, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    # ─── 正文 ──────────────────────────────

    def add_text(self, text):
        self.set_text_color(*TEXT_BODY)
        self.set_font('CN', '', 10)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def add_conclusion(self, text, status='hold'):
        """
        结论高亮。
        status: 'hold' = 假设成立 (绿)，'reject' = 被推翻 (红)，
                'unknown' = 数据不足 (橙)
        """
        color = {'hold': GREEN, 'reject': RED, 'unknown': ORANGE}.get(status, GREEN)
        self.ln(1)
        self.set_text_color(*color)
        self.set_font('CN', 'B', 10)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def add_action(self, text):
        """建议动作框：深紫背景 + 粉色左边框 + 粉色文字"""
        self.ln(2)
        y_start = self.get_y()
        self.set_x(17)
        self.set_fill_color(*BG_PURPLE)
        self.set_text_color(*PINK)
        self.set_font('CN', 'B', 10)
        self.multi_cell(self.w - 32, 7, text, fill=True, align='L')
        y_end = self.get_y()
        # 左侧粉色边框（绘制在背景上）
        self.set_fill_color(*PINK)
        self.rect(15, y_start, 1.4, max(y_end - y_start, 4), 'F')
        self.set_text_color(*TEXT_BODY)
        self.ln(2)

    def add_warning(self, text, level='warn'):
        """
        风险/局限性标签。
        level: 'warn' = 橙色 (小样本/推断/未做时间归因校正等)
               'danger' = 红色 (数据不足等)
        """
        color = ORANGE if level == 'warn' else RED
        self.set_text_color(*color)
        self.set_font('CN', 'B', 9)
        self.multi_cell(0, 5, text)
        self.set_text_color(*TEXT_BODY)
        self.ln(1)

    # ─── 图表与表格 ────────────────────────

    def add_chart(self, image_path, caption=None, width=None):
        """
        嵌入图表（图表本身应当用 chart_style.apply_style('dark') 生成，
        这样背景色才能与 PDF 一致）。
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f'图表文件不存在: {image_path}')
        if width is None:
            width = self.w - 30
        # 计算高度（pillow 已在依赖里，失败直接抛错，避免 fallback 误判分页）
        from PIL import Image
        with Image.open(image_path) as im:
            iw, ih = im.size
        display_h = width * ih / iw
        # 自动分页保护
        if self.get_y() + display_h + 12 > self.h - self.b_margin:
            self.add_page()
        x = (self.w - width) / 2
        y = self.get_y() + 2
        self.image(image_path, x=x, y=y, w=width)
        self.set_y(y + display_h + 2)
        if caption:
            self.set_font('CN', '', 8)
            self.set_text_color(*TEXT_MUTED)
            self.cell(0, 5, caption, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def add_table(self, headers, rows, roi_col=None):
        """
        表格。第一列加粗。支持自动分页（跨页时表头会重绘）和长内容截断。
        roi_col: int 列索引，该列数值 >=1 显示绿色，<1 显示红色（用于 ROI 等阈值列）。
        """
        n = len(headers)
        col_w = (self.w - 2 * self.l_margin) / n
        header_h = 8
        row_h = 7

        def _truncate(text, max_w):
            """按字符串宽度截断长内容，超出时尾部加 …。"""
            s = str(text)
            if self.get_string_width(s) <= max_w:
                return s
            ellipsis = '…'
            ell_w = self.get_string_width(ellipsis)
            # 二分截断更稳一些，但中文字符宽度均匀，线性裁剪足够
            while s and self.get_string_width(s) + ell_w > max_w:
                s = s[:-1]
            return s + ellipsis

        def _draw_header():
            self.set_fill_color(*BG_TABLE_HEADER)
            self.set_text_color(*TEXT_BODY)
            self.set_font('CN', 'B', 9)
            for h in headers:
                self.cell(col_w, header_h, _truncate(h, col_w - 2), fill=True, align='C')
            self.ln()

        _draw_header()
        # 数据行
        for i, row in enumerate(rows):
            # 分页保护：剩余空间不足以放下一行时换页并重绘表头
            if self.get_y() + row_h > self.h - self.b_margin:
                self.add_page()
                _draw_header()
            fill = BG_TABLE_ROW_A if i % 2 == 0 else BG_TABLE_ROW_B
            self.set_fill_color(*fill)
            for j, cell in enumerate(row):
                if j == roi_col:
                    try:
                        v = float(str(cell).replace(',', '').replace('%', ''))
                        self.set_text_color(*(GREEN if v >= 1 else RED))
                    except (ValueError, TypeError):
                        self.set_text_color(*TEXT_BODY)
                    self.set_font('CN', 'B', 9)
                elif j == 0:
                    self.set_text_color(*TEXT_BODY)
                    self.set_font('CN', 'B', 9)
                else:
                    self.set_text_color(*TEXT_BODY)
                    self.set_font('CN', '', 9)
                self.cell(col_w, row_h, _truncate(cell, col_w - 2), fill=True, align='C')
            self.ln()
        self.set_text_color(*TEXT_BODY)
        self.ln(2)

    # ─── 输出 ──────────────────────────────

    def save(self, filepath):
        self.output(filepath)
        return filepath
