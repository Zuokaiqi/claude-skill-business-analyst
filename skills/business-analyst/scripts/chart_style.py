"""
数据分析技能 - 图表样式配置
使用方式: exec(open("<此文件路径>").read())
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# ── 中文字体支持 ──
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'PingFang SC']
plt.rcParams['axes.unicode_minus'] = False

# ── 配色方案 ──
# 主色：粉色和蓝色（与参考报告风格一致）
COLOR_PRIMARY = '#E91E8C'    # 粉色 - 主要数据
COLOR_SECONDARY = '#4A9EF5'  # 蓝色 - 对比数据
COLOR_ACCENT = '#F5A623'     # 橙色 - 强调
COLOR_SUCCESS = '#2ECC71'    # 绿色 - 正向指标
COLOR_DANGER = '#E74C3C'     # 红色 - 负向指标
COLOR_PURPLE = '#7B68EE'     # 紫色 - 补充

PALETTE = [COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT, COLOR_PURPLE, COLOR_SUCCESS, COLOR_DANGER]
PALETTE_CONTRAST = [COLOR_PRIMARY, COLOR_SECONDARY]  # 双色对比

# ── 深色主题 ──
DARK_BG = '#1A1A2E'
DARK_SURFACE = '#16213E'
DARK_TEXT = '#E8E8E8'
DARK_GRID = '#2A2A4A'

# ── 浅色主题（默认） ──
LIGHT_BG = '#FFFFFF'
LIGHT_TEXT = '#333333'
LIGHT_GRID = '#E0E0E0'


def apply_style(theme='light', figsize=(10, 6)):
    """
    应用图表样式。
    theme: 'light' 或 'dark'
    """
    if theme == 'dark':
        plt.rcParams.update({
            'figure.facecolor': DARK_BG,
            'axes.facecolor': DARK_SURFACE,
            'text.color': DARK_TEXT,
            'axes.labelcolor': DARK_TEXT,
            'xtick.color': DARK_TEXT,
            'ytick.color': DARK_TEXT,
            'axes.edgecolor': DARK_GRID,
            'grid.color': DARK_GRID,
        })
    else:
        plt.rcParams.update({
            'figure.facecolor': LIGHT_BG,
            'axes.facecolor': LIGHT_BG,
            'text.color': LIGHT_TEXT,
            'axes.labelcolor': LIGHT_TEXT,
            'xtick.color': LIGHT_TEXT,
            'ytick.color': LIGHT_TEXT,
            'axes.edgecolor': LIGHT_GRID,
            'grid.color': LIGHT_GRID,
        })

    plt.rcParams.update({
        'figure.figsize': figsize,
        'figure.dpi': 150,
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
    """保存图表"""
    if tight:
        fig.tight_layout()
    fig.savefig(filename, bbox_inches='tight', facecolor=fig.get_facecolor())
    print(f"图表已保存: {filename}")


# 默认应用浅色主题
apply_style('light')
