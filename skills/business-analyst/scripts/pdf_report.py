"""
数据分析技能 - PDF 报告生成器

历史版本的PDF渲染封装。v3起默认路径切换到Playwright+Paged.js，
本脚本保留供需要fpdf2的执行环境作为可选参考。

依赖: fpdf2 (>=2.7), pillow

标准用法：

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / '.claude' / 'skills' / 'business-analyst' / 'scripts'))
    from pdf_report import Report

    r = Report(title='2026 Q1 渠道 ROI 分析', subtitle='2026-01-01 ~ 2026-03-31', theme='ocean')
    r.add_cover(metrics=[
        ('总消耗', '234万', '同比 +12%'),
        ('总回款', '1180万', '同比 +28%'),
        ('整体 ROI', '5.04', '行业均值 3.2'),
        ('签约客户', '342', '单客成本 6842'),
    ])

    r.new_section()
    r.add_h1('维度一：渠道效率对比')
    r.add_hypothesis_label(1, '小红书 ROI 显著优于抖音信息流')
    r.add_text('小红书消耗 21 万，回款 84 万，简单 ROI 3.95...')
    r.add_warning('未做时间归因校正，加盟周期 1-3 个月', level='warn')
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

可用主题: midnight(默认), ocean, forest, ember, lavender, minimal
"""
import os
import sys
from fpdf import FPDF
from fpdf.enums import XPos, YPos

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from chart_style import THEMES, get_theme, _hex_to_rgb, find_chinese_font_path

# 模块级向后兼容常量，始终指向 midnight 主题
BG_PAGE          = (26, 26, 46)
BG_CARD          = (35, 40, 74)
BG_TABLE_HEADER  = (54, 55, 88)
BG_TABLE_ROW_A   = (30, 35, 58)
BG_TABLE_ROW_B   = (26, 30, 50)
BG_PURPLE        = (47, 35, 78)

TEXT_BODY  = (190, 195, 215)
TEXT_TITLE = (255, 255, 255)
TEXT_MUTED = (140, 145, 170)

PINK   = (233, 30, 140)
BLUE   = (74, 158, 245)
ORANGE = (245, 166, 35)
GREEN  = (46, 204, 113)
RED    = (231, 76, 60)

# fpdf2子集化时无法正确包含的Unicode字符替换表
_CHAR_REPLACEMENTS = {
    '\u2014': '-',    # em-dash
    '\u2013': '-',    # en-dash
    '\u2018': "'",    # left single quote
    '\u2019': "'",    # right single quote
    '\u201C': '"',    # left double quote
    '\u201D': '"',    # right double quote
    '\u2026': '...',  # ellipsis
    '\u00A0': ' ',    # non-breaking space
    '\uFEFF': '',     # BOM
    '\u3000': ' ',    # ideographic space
}


class Report(FPDF):
    """商业数据分析 PDF 报告"""

    def __init__(self, title='数据分析报告', subtitle='', theme='midnight'):
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

        t = get_theme(theme)
        self._bg_page          = t['pdf_page_bg']
        self._bg_card          = t['pdf_surface_bg']
        self._bg_table_header  = t['pdf_table_header']
        self._bg_table_row_a   = t['pdf_table_row_a']
        self._bg_table_row_b   = t['pdf_table_row_b']
        self._bg_highlight     = t['pdf_highlight_bg']
        self._text_body        = t['pdf_text']
        self._text_title       = t['pdf_title']
        self._text_muted       = t['pdf_muted']
        self._color_primary    = _hex_to_rgb(t['primary'])
        self._color_secondary  = _hex_to_rgb(t['secondary'])
        self._color_accent     = _hex_to_rgb(t['accent'])
        self._color_success    = _hex_to_rgb(t['success'])
        self._color_danger     = _hex_to_rgb(t['danger'])

    def _sanitize(self, text):
        s = str(text)
        for old, new in _CHAR_REPLACEMENTS.items():
            s = s.replace(old, new)
        return s

    # page decoration

    def header(self):
        self.set_fill_color(*self._bg_page)
        self.rect(0, 0, self.w, self.h, 'F')
        self.set_xy(self.l_margin, self.t_margin)

    def footer(self):
        self.set_y(-12)
        self.set_font('CN', '', 8)
        self.set_text_color(*self._text_muted)
        self.cell(0, 6, self._sanitize(f'{self.report_title}    -  {self.page_no()}  -'), align='C')

    # cover

    def add_cover(self, metrics=None):
        self.add_page()
        self.set_fill_color(*self._color_primary)
        self.rect(0, 0, self.w, 70, 'F')
        self.set_xy(15, 22)
        self.set_text_color(*self._text_title)
        self.set_font('CN', 'B', 24)
        self.cell(0, 14, self._sanitize(self.report_title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        if self.report_subtitle:
            self.set_x(15)
            self.set_font('CN', '', 12)
            self.cell(0, 8, self._sanitize(self.report_subtitle))
        if metrics:
            self.set_y(90)
            self._draw_metric_grid(metrics)

    def _draw_metric_grid(self, metrics):
        metrics = list(metrics)[:4]
        card_w = (self.w - 30 - 6) / 2
        card_h = 36
        x0, y0 = 15, self.get_y()
        for i, item in enumerate(metrics):
            name, value, desc = (list(item) + ['', ''])[:3]
            row, col = divmod(i, 2)
            x = x0 + col * (card_w + 6)
            y = y0 + row * (card_h + 6)
            self.set_fill_color(*self._bg_card)
            self.rect(x, y, card_w, card_h, 'F')
            self.set_xy(x + 5, y + 5)
            self.set_text_color(*self._text_muted)
            self.set_font('CN', '', 9)
            self.cell(card_w - 10, 5, self._sanitize(name))
            self.set_xy(x + 5, y + 12)
            self.set_text_color(*self._color_primary)
            self.set_font('CN', 'B', 20)
            self.cell(card_w - 10, 11, self._sanitize(value))
            self.set_xy(x + 5, y + 25)
            self.set_text_color(*self._text_muted)
            self.set_font('CN', '', 8)
            self.cell(card_w - 10, 5, self._sanitize(desc))
        self.set_y(y0 + 2 * (card_h + 6) + 6)

    def add_metric_cards(self, metrics):
        self.ln(4)
        self._draw_metric_grid(metrics)

    # section and headings

    def new_section(self):
        self.add_page()

    def add_h1(self, text):
        self.ln(3)
        y = self.get_y()
        self.set_fill_color(*self._color_primary)
        self.rect(15, y + 2, 1.4, 9, 'F')
        self.set_xy(18, y)
        self.set_text_color(*self._text_title)
        self.set_font('CN', 'B', 15)
        self.cell(0, 12, self._sanitize(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def add_h2(self, text):
        self.ln(2)
        self.set_text_color(*self._text_title)
        self.set_font('CN', 'B', 12)
        self.cell(0, 8, self._sanitize(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def add_hypothesis_label(self, idx, summary):
        self.ln(1)
        text = self._sanitize(f'  验证假设 {idx}: {summary}  ')
        self.set_fill_color(*self._bg_highlight)
        self.set_text_color(*self._color_accent)
        self.set_font('CN', '', 9)
        w = self.get_string_width(text) + 4
        self.cell(w, 7, text, fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    # body content

    def add_text(self, text):
        self.set_text_color(*self._text_body)
        self.set_font('CN', '', 10)
        self.multi_cell(0, 6, self._sanitize(text), align='L')
        self.ln(1)

    def add_conclusion(self, text, status='hold'):
        color = {
            'hold': self._color_success,
            'reject': self._color_danger,
            'unknown': self._color_accent,
        }.get(status, self._color_success)
        self.ln(1)
        self.set_text_color(*color)
        self.set_font('CN', 'B', 10)
        self.multi_cell(0, 6, self._sanitize(text), align='L')
        self.ln(1)

    def add_action(self, text):
        self.ln(2)
        y_start = self.get_y()
        self.set_x(17)
        self.set_fill_color(*self._bg_highlight)
        self.set_text_color(*self._color_primary)
        self.set_font('CN', 'B', 10)
        self.multi_cell(self.w - 32, 7, self._sanitize(text), fill=True, align='L')
        y_end = self.get_y()
        self.set_fill_color(*self._color_primary)
        self.rect(15, y_start, 1.4, max(y_end - y_start, 4), 'F')
        self.set_text_color(*self._text_body)
        self.ln(2)

    def add_warning(self, text, level='warn'):
        color = self._color_accent if level == 'warn' else self._color_danger
        self.set_text_color(*color)
        self.set_font('CN', 'B', 9)
        self.multi_cell(0, 5, self._sanitize(text), align='L')
        self.set_text_color(*self._text_body)
        self.ln(1)

    # charts and tables

    def add_chart(self, image_path, caption=None, width=None):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f'图表文件不存在: {image_path}')
        if width is None:
            width = self.w - 30
        from PIL import Image
        with Image.open(image_path) as im:
            iw, ih = im.size
        display_h = width * ih / iw
        if self.get_y() + display_h + 12 > self.h - self.b_margin:
            self.add_page()
        x = (self.w - width) / 2
        y = self.get_y() + 2
        self.image(image_path, x=x, y=y, w=width)
        self.set_y(y + display_h + 2)
        if caption:
            self.set_font('CN', '', 8)
            self.set_text_color(*self._text_muted)
            self.cell(0, 5, self._sanitize(caption), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def add_table(self, headers, rows, roi_col=None):
        n = len(headers)
        col_w = (self.w - 2 * self.l_margin) / n
        header_h = 8
        row_h = 7

        def _truncate(text, max_w):
            s = self._sanitize(text)
            if self.get_string_width(s) <= max_w:
                return s
            ellipsis = '...'
            ell_w = self.get_string_width(ellipsis)
            while s and self.get_string_width(s) + ell_w > max_w:
                s = s[:-1]
            return s + ellipsis

        def _draw_header():
            self.set_fill_color(*self._bg_table_header)
            self.set_text_color(*self._text_body)
            self.set_font('CN', 'B', 9)
            for h in headers:
                self.cell(col_w, header_h, _truncate(h, col_w - 2), fill=True, align='C')
            self.ln()

        _draw_header()
        for i, row in enumerate(rows):
            if self.get_y() + row_h > self.h - self.b_margin:
                self.add_page()
                _draw_header()
            fill = self._bg_table_row_a if i % 2 == 0 else self._bg_table_row_b
            self.set_fill_color(*fill)
            for j, cell in enumerate(row):
                if j == roi_col:
                    try:
                        v = float(str(cell).replace(',', '').replace('%', ''))
                        self.set_text_color(*(self._color_success if v >= 1 else self._color_danger))
                    except (ValueError, TypeError):
                        self.set_text_color(*self._text_body)
                    self.set_font('CN', 'B', 9)
                elif j == 0:
                    self.set_text_color(*self._text_body)
                    self.set_font('CN', 'B', 9)
                else:
                    self.set_text_color(*self._text_body)
                    self.set_font('CN', '', 9)
                self.cell(col_w, row_h, _truncate(cell, col_w - 2), fill=True, align='C')
            self.ln()
        self.set_text_color(*self._text_body)
        self.ln(2)

    # output

    def save(self, filepath):
        self.output(filepath)
        return filepath
