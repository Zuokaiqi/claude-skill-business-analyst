"""
数据分析技能 - 图表样式 + 中文字体工具

标准用法（与 PDF 报告样式严格对齐）：

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.home() / '.claude' / 'skills' / 'business-analyst' / 'scripts'))
    from chart_style import apply_style, save_chart, COLOR_PRIMARY, COLOR_SECONDARY, PALETTE
    apply_style('dark')   # 深色，与 PDF 报告一致；嵌入 PDF 时必须用这个

如果需要单独导出浅色背景图（极少用），传 apply_style('light')。
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager

# ── 配色（与 references/report_style.md 严格对应） ──
COLOR_PRIMARY = '#E91E8C'    # 粉色 - 主要数据
COLOR_SECONDARY = '#4A9EF5'  # 蓝色 - 对比数据
COLOR_ACCENT = '#F5A623'     # 橙色 - 强调 / 风险标签
COLOR_SUCCESS = '#2ECC71'    # 绿色 - 正向 / 假设成立
COLOR_DANGER = '#E74C3C'     # 红色 - 负向 / 假设被推翻
COLOR_PURPLE = '#7B68EE'     # 紫色 - 补充

PALETTE = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_PURPLE, COLOR_SUCCESS, COLOR_DANGER]
PALETTE_CONTRAST = [COLOR_PRIMARY, COLOR_SECONDARY]

# ── 深色主题（与 PDF 报告完全一致，不要随意改） ──
DARK_BG = '#1A1A2E'        # 页面背景
DARK_SURFACE = '#23284A'    # 卡片 / 绘图区背景
DARK_TEXT = '#BEC3D7'       # 正文
DARK_TITLE = '#FFFFFF'      # 标题
DARK_GRID = '#363758'       # 网格 / 表头

# ── 浅色主题（备选） ──
LIGHT_BG = '#FFFFFF'
LIGHT_TEXT = '#333333'
LIGHT_GRID = '#E0E0E0'


# ─────────────────────────────────────────────
# 中文字体跨平台探测
# ─────────────────────────────────────────────

_FONT_CANDIDATES_REGULAR = [
    # Windows
    'C:/Windows/Fonts/msyh.ttc',
    'C:/Windows/Fonts/msyh.ttf',
    'C:/Windows/Fonts/simhei.ttf',
    'C:/Windows/Fonts/simsun.ttc',
    # macOS
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/Library/Fonts/Arial Unicode.ttf',
    # Linux
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
]

_FONT_CANDIDATES_BOLD = [
    'C:/Windows/Fonts/msyhbd.ttc',
    'C:/Windows/Fonts/msyhbd.ttf',
    'C:/Windows/Fonts/simhei.ttf',  # SimHei 本身较粗
    '/System/Library/Fonts/PingFang.ttc',
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
]


def find_chinese_font_path(bold=False):
    """跨平台中文字体路径探测。返回首个存在的字体文件绝对路径，找不到返回 None。"""
    candidates = _FONT_CANDIDATES_BOLD if bold else _FONT_CANDIDATES_REGULAR
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def _register_chinese_font_for_matplotlib():
    """把找到的中文字体注册到 matplotlib，返回字体家族名（供 rcParams 使用）。"""
    path = find_chinese_font_path()
    if not path:
        return None
    try:
        font_manager.fontManager.addfont(path)
        return font_manager.FontProperties(fname=path).get_name()
    except Exception:
        return None


# 模块加载时立即注册中文字体
_cn_font_name = _register_chinese_font_for_matplotlib()
_default_sans = ['SimHei', 'Microsoft YaHei', 'PingFang SC', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
if _cn_font_name and _cn_font_name not in _default_sans:
    _default_sans = [_cn_font_name] + _default_sans
plt.rcParams['font.sans-serif'] = _default_sans
plt.rcParams['axes.unicode_minus'] = False


# ─────────────────────────────────────────────
# 主题与图表工具
# ─────────────────────────────────────────────

def apply_style(theme='dark', figsize=(10, 6)):
    """
    应用图表全局样式。
    theme: 'dark' (默认，与 PDF 报告一致) 或 'light'
    """
    if theme == 'dark':
        plt.rcParams.update({
            'figure.facecolor': DARK_BG,
            'axes.facecolor': DARK_SURFACE,
            'savefig.facecolor': DARK_BG,
            'savefig.edgecolor': DARK_BG,
            'text.color': DARK_TEXT,
            'axes.labelcolor': DARK_TEXT,
            'axes.titlecolor': DARK_TITLE,
            'xtick.color': DARK_TEXT,
            'ytick.color': DARK_TEXT,
            'axes.edgecolor': DARK_GRID,
            'grid.color': DARK_GRID,
        })
    else:
        plt.rcParams.update({
            'figure.facecolor': LIGHT_BG,
            'axes.facecolor': LIGHT_BG,
            'savefig.facecolor': LIGHT_BG,
            'savefig.edgecolor': LIGHT_BG,
            'text.color': LIGHT_TEXT,
            'axes.labelcolor': LIGHT_TEXT,
            'axes.titlecolor': LIGHT_TEXT,
            'xtick.color': LIGHT_TEXT,
            'ytick.color': LIGHT_TEXT,
            'axes.edgecolor': LIGHT_GRID,
            'grid.color': LIGHT_GRID,
        })

    plt.rcParams.update({
        'figure.figsize': figsize,
        'figure.dpi': 150,
        'savefig.dpi': 150,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
    })

    sns.set_palette(PALETTE)


def add_bar_labels(ax, fmt='{:.1f}', fontsize=9, offset=3):
    """在柱状图上添加数据标签"""
    for container in ax.containers:
        labels = [fmt.format(v.get_height()) if v.get_height() != 0 else '' for v in container]
        ax.bar_label(container, labels=labels, fontsize=fontsize, padding=offset)


def add_hbar_labels(ax, fmt='{:.1f}', fontsize=9, offset=3):
    """在水平柱状图上添加数据标签"""
    for container in ax.containers:
        labels = [fmt.format(v.get_width()) if v.get_width() != 0 else '' for v in container]
        ax.bar_label(container, labels=labels, fontsize=fontsize, padding=offset)


def save_chart(fig, filename, tight=True):
    """保存图表，背景与当前主题一致。返回保存路径。"""
    if tight:
        fig.tight_layout()
    fig.savefig(filename, bbox_inches='tight', facecolor=fig.get_facecolor())
    return filename


# 模块加载时默认应用深色主题（与 PDF 报告样式一致）
apply_style('dark')
