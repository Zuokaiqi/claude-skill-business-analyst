"""
数据分析技能 - 图表样式 + 中文字体工具

标准用法（与 PDF 报告样式严格对齐）：

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / '.claude' / 'skills' / 'business-analyst' / 'scripts'))
    from chart_style import apply_style, save_chart, COLOR_PRIMARY, COLOR_SECONDARY, PALETTE
    apply_style('midnight')   # 深色，与 PDF 报告一致；嵌入 PDF 时必须用这个

旧写法 apply_style('dark') 等同 midnight，apply_style('light') 等同 minimal，向后兼容。
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager


def _hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


THEMES = {
    'midnight': {
        'page_bg':    '#1A1A2E',
        'surface_bg': '#23284A',
        'text':       '#BEC3D7',
        'title':      '#FFFFFF',
        'grid':       '#363758',
        'primary':    '#E91E8C',
        'secondary':  '#4A9EF5',
        'accent':     '#F5A623',
        'success':    '#2ECC71',
        'danger':     '#E74C3C',
        'purple':     '#7B68EE',
        'pdf_page_bg':     (26, 26, 46),
        'pdf_surface_bg':  (35, 40, 74),
        'pdf_table_header':(54, 55, 88),
        'pdf_table_row_a': (30, 35, 58),
        'pdf_table_row_b': (26, 30, 50),
        'pdf_highlight_bg':(47, 35, 78),
        'pdf_text':        (190, 195, 215),
        'pdf_title':       (255, 255, 255),
        'pdf_muted':       (140, 145, 170),
    },
    'ocean': {
        'page_bg':    '#0B1929',
        'surface_bg': '#132F4C',
        'text':       '#B0C4DE',
        'title':      '#E8F4FD',
        'grid':       '#1E3F60',
        'primary':    '#3B82F6',
        'secondary':  '#22D3EE',
        'accent':     '#F59E0B',
        'success':    '#06D6A0',
        'danger':     '#EF4444',
        'purple':     '#818CF8',
        'pdf_page_bg':     (11, 25, 41),
        'pdf_surface_bg':  (19, 47, 76),
        'pdf_table_header':(30, 63, 96),
        'pdf_table_row_a': (15, 35, 58),
        'pdf_table_row_b': (11, 28, 48),
        'pdf_highlight_bg':(20, 55, 90),
        'pdf_text':        (176, 196, 222),
        'pdf_title':       (232, 244, 253),
        'pdf_muted':       (120, 150, 180),
    },
    'forest': {
        'page_bg':    '#0A1A14',
        'surface_bg': '#12302A',
        'text':       '#A7C4B5',
        'title':      '#E8F5EE',
        'grid':       '#1A4035',
        'primary':    '#10B981',
        'secondary':  '#34D399',
        'accent':     '#F97316',
        'success':    '#4ADE80',
        'danger':     '#FB7185',
        'purple':     '#A78BFA',
        'pdf_page_bg':     (10, 26, 20),
        'pdf_surface_bg':  (18, 48, 42),
        'pdf_table_header':(26, 64, 53),
        'pdf_table_row_a': (14, 38, 32),
        'pdf_table_row_b': (10, 30, 25),
        'pdf_highlight_bg':(20, 55, 45),
        'pdf_text':        (167, 196, 181),
        'pdf_title':       (232, 245, 238),
        'pdf_muted':       (110, 150, 130),
    },
    'ember': {
        'page_bg':    '#1A1008',
        'surface_bg': '#2D1F10',
        'text':       '#D4B896',
        'title':      '#FFF8EE',
        'grid':       '#4A3018',
        'primary':    '#F59E0B',
        'secondary':  '#FBBF24',
        'accent':     '#8B5CF6',
        'success':    '#86EFAC',
        'danger':     '#FCA5A5',
        'purple':     '#C084FC',
        'pdf_page_bg':     (26, 16, 8),
        'pdf_surface_bg':  (45, 31, 16),
        'pdf_table_header':(74, 48, 24),
        'pdf_table_row_a': (36, 24, 12),
        'pdf_table_row_b': (28, 19, 9),
        'pdf_highlight_bg':(60, 40, 18),
        'pdf_text':        (212, 184, 150),
        'pdf_title':       (255, 248, 238),
        'pdf_muted':       (160, 130, 100),
    },
    'lavender': {
        'page_bg':    '#13101F',
        'surface_bg': '#1E1A32',
        'text':       '#C4B8E8',
        'title':      '#F0ECFF',
        'grid':       '#2E2850',
        'primary':    '#A78BFA',
        'secondary':  '#C4B5FD',
        'accent':     '#06B6D4',
        'success':    '#6EE7B7',
        'danger':     '#F9A8D4',
        'purple':     '#E879F9',
        'pdf_page_bg':     (19, 16, 31),
        'pdf_surface_bg':  (30, 26, 50),
        'pdf_table_header':(46, 40, 80),
        'pdf_table_row_a': (24, 20, 42),
        'pdf_table_row_b': (19, 16, 36),
        'pdf_highlight_bg':(40, 32, 68),
        'pdf_text':        (196, 184, 232),
        'pdf_title':       (240, 236, 255),
        'pdf_muted':       (145, 130, 185),
    },
    'minimal': {
        'page_bg':    '#FFFFFF',
        'surface_bg': '#F8FAFC',
        'text':       '#475569',
        'title':      '#1E293B',
        'grid':       '#E2E8F0',
        'primary':    '#2563EB',
        'secondary':  '#3B82F6',
        'accent':     '#F97316',
        'success':    '#16A34A',
        'danger':     '#DC2626',
        'purple':     '#7C3AED',
        'pdf_page_bg':     (255, 255, 255),
        'pdf_surface_bg':  (248, 250, 252),
        'pdf_table_header':(226, 232, 240),
        'pdf_table_row_a': (248, 250, 252),
        'pdf_table_row_b': (241, 245, 249),
        'pdf_highlight_bg':(219, 234, 254),
        'pdf_text':        (71, 85, 105),
        'pdf_title':       (30, 41, 59),
        'pdf_muted':       (148, 163, 184),
    },
}

# 向后兼容别名
_THEME_ALIASES = {'dark': 'midnight', 'light': 'minimal'}

# ── midnight主题的legacy变量（向后兼容，值固定指向midnight） ──
DARK_BG      = THEMES['midnight']['page_bg']
DARK_SURFACE = THEMES['midnight']['surface_bg']
DARK_TEXT    = THEMES['midnight']['text']
DARK_TITLE   = THEMES['midnight']['title']
DARK_GRID    = THEMES['midnight']['grid']

LIGHT_BG   = THEMES['minimal']['page_bg']
LIGHT_TEXT = THEMES['minimal']['text']
LIGHT_GRID = THEMES['minimal']['grid']

# ── 全局配色变量（随当前主题变化） ──
COLOR_PRIMARY   = THEMES['midnight']['primary']
COLOR_SECONDARY = THEMES['midnight']['secondary']
COLOR_ACCENT    = THEMES['midnight']['accent']
COLOR_SUCCESS   = THEMES['midnight']['success']
COLOR_DANGER    = THEMES['midnight']['danger']
COLOR_PURPLE    = THEMES['midnight']['purple']

PALETTE          = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_PURPLE, COLOR_SUCCESS, COLOR_DANGER]
PALETTE_CONTRAST = [COLOR_PRIMARY, COLOR_SECONDARY]

_active_theme = 'midnight'


# ─────────────────────────────────────────────
# 中文字体跨平台探测
# ─────────────────────────────────────────────

_FONT_CANDIDATES_REGULAR = [
    'C:/Windows/Fonts/msyh.ttc',
    'C:/Windows/Fonts/msyh.ttf',
    'C:/Windows/Fonts/simhei.ttf',
    'C:/Windows/Fonts/simsun.ttc',
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/Library/Fonts/Arial Unicode.ttf',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
]

_FONT_CANDIDATES_BOLD = [
    'C:/Windows/Fonts/msyhbd.ttc',
    'C:/Windows/Fonts/msyhbd.ttf',
    'C:/Windows/Fonts/simhei.ttf',
    '/System/Library/Fonts/PingFang.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
]


def find_chinese_font_path(bold=False):
    candidates = _FONT_CANDIDATES_BOLD if bold else _FONT_CANDIDATES_REGULAR
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def _register_chinese_font_for_matplotlib():
    path = find_chinese_font_path()
    if not path:
        return None
    try:
        font_manager.fontManager.addfont(path)
        return font_manager.FontProperties(fname=path).get_name()
    except Exception:
        return None


_cn_font_name = _register_chinese_font_for_matplotlib()
_default_sans = ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
if _cn_font_name and _cn_font_name not in _default_sans:
    _default_sans = [_cn_font_name] + _default_sans
plt.rcParams['font.sans-serif'] = _default_sans
plt.rcParams['axes.unicode_minus'] = False


# ─────────────────────────────────────────────
# 主题查询
# ─────────────────────────────────────────────

def get_theme(name):
    name = _THEME_ALIASES.get(name, name)
    if name not in THEMES:
        raise ValueError(f"未知主题 {name!r}，可用: {list_themes()}")
    return THEMES[name]


def current_theme():
    return THEMES[_active_theme]


def list_themes():
    return list(THEMES.keys())


# ─────────────────────────────────────────────
# 主题与图表工具
# ─────────────────────────────────────────────

def apply_style(theme='midnight', figsize=(10, 6)):
    """
    应用图表全局样式。
    theme: 'midnight'(默认) / 'ocean' / 'forest' / 'ember' / 'lavender' / 'minimal'
           旧写法 'dark'(等同midnight) / 'light'(等同minimal) 仍然有效
    """
    global _active_theme
    global COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_SUCCESS, COLOR_DANGER, COLOR_PURPLE
    global PALETTE, PALETTE_CONTRAST

    theme = _THEME_ALIASES.get(theme, theme)
    if theme not in THEMES:
        raise ValueError(f"未知主题 {theme!r}，可用: {list_themes()}")

    t = THEMES[theme]
    _active_theme = theme

    COLOR_PRIMARY   = t['primary']
    COLOR_SECONDARY = t['secondary']
    COLOR_ACCENT    = t['accent']
    COLOR_SUCCESS   = t['success']
    COLOR_DANGER    = t['danger']
    COLOR_PURPLE    = t['purple']
    PALETTE          = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_PURPLE, COLOR_SUCCESS, COLOR_DANGER]
    PALETTE_CONTRAST = [COLOR_PRIMARY, COLOR_SECONDARY]

    plt.rcParams.update({
        'figure.facecolor':  t['page_bg'],
        'axes.facecolor':    t['surface_bg'],
        'savefig.facecolor': t['page_bg'],
        'savefig.edgecolor': t['page_bg'],
        'text.color':        t['text'],
        'axes.labelcolor':   t['text'],
        'axes.titlecolor':   t['title'],
        'xtick.color':       t['text'],
        'ytick.color':       t['text'],
        'axes.edgecolor':    t['grid'],
        'grid.color':        t['grid'],
        'figure.figsize':    figsize,
        'figure.dpi':        150,
        'savefig.dpi':       150,
        'axes.spines.top':   False,
        'axes.spines.right': False,
        'axes.grid':         True,
        'grid.alpha':        0.3,
        'font.size':         11,
        'axes.titlesize':    14,
        'axes.titleweight':  'bold',
    })

    sns.set_palette(PALETTE)


def add_bar_labels(ax, fmt='{:.1f}', fontsize=9, offset=3):
    for container in ax.containers:
        labels = [fmt.format(v.get_height()) if v.get_height() != 0 else '' for v in container]
        ax.bar_label(container, labels=labels, fontsize=fontsize, padding=offset)


def add_hbar_labels(ax, fmt='{:.1f}', fontsize=9, offset=3):
    for container in ax.containers:
        labels = [fmt.format(v.get_width()) if v.get_width() != 0 else '' for v in container]
        ax.bar_label(container, labels=labels, fontsize=fontsize, padding=offset)


def save_chart(fig, filename, tight=True):
    if tight:
        fig.tight_layout()
    fig.savefig(filename, bbox_inches='tight', facecolor=fig.get_facecolor())
    return filename


apply_style('midnight')
