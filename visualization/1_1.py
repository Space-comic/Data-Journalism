import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# 1. 准备数据
events = [
    ("2025-01", "特朗普启动\n关税调查"),
    ("2025-03", "BIS实体清单\n大规模更新"),
    ("2025-05", "智库聚焦\n阿联酋转运漏洞"),
    ("2025-07", "美方发布\nAI行动计划"),
    ("2025-09", "只租不卖\n政策构想讨论"),
    ("2025-12", "复合对抗\n态势最终形成")
]

# 转换时间格式
dates = [datetime.strptime(d, "%Y-%m") for d, e in events]
names = [e for d, e in events]

# 2. 设置LaTeX友好风格 - 紧凑布局
plt.rcParams.update({
    'font.sans-serif': ['SimHei'],
    'axes.unicode_minus': False,
    'font.size': 20,  # 增大基础字体
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 10,
    'figure.constrained_layout.use': True,
    'figure.constrained_layout.h_pad': 0.05,  # 减小水平padding
    'figure.constrained_layout.w_pad': 0.05,  # 减小垂直padding
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02  # 减小保存时的边距
})

# 3. 创建适合LaTeX双栏的图形 (宽度大，高度小)
fig, ax = plt.subplots(figsize=(12, 3.5))  # 宽高比适合双栏

# 4. 绘制时间轴线条 - 更靠近中心
ax.axhline(0, color="navy", linewidth=2.5, zorder=1)

# 5. 绘制节点 - 减小垂直距离
# 调整高度，使标注更紧凑
levels = [0.5, -0.5, 0.5, -0.5, 0.5, -0.5]  # 减小垂直偏移量
line_lengths = [0.3, -0.3, 0.3, -0.3, 0.3, -0.3]  # 连接线长度更短

# 绘制连接线
for date, length in zip(dates, line_lengths):
    ax.vlines(date, 0, length, color="grey", linestyle="-", 
              linewidth=1.5, alpha=0.6, zorder=2)

# 绘制节点圆点
ax.scatter(dates, [0]*len(dates), c="navy", s=80, zorder=3, 
           edgecolors="white", linewidth=2)

# 6. 标注文字 - 优化布局避免重叠
for i, (date, name) in enumerate(zip(dates, names)):
    # 根据位置调整文本偏移
    if levels[i] > 0:
        va = 'bottom'
        y_offset = 2
    else:
        va = 'top'
        y_offset = -2
    
    ax.annotate(name, xy=(date, line_lengths[i]),
                xytext=(0, y_offset), 
                textcoords="offset points",
                ha="center", va=va,
                fontsize=20,  # 增大标注字体
                fontweight='bold',
                linespacing=1.2,  # 优化多行间距
                bbox=dict(boxstyle='round,pad=0.25', 
                         fc='aliceblue', 
                         ec='navy', 
                         alpha=0.9,
                         linewidth=1.2))

# 7. 格式化坐标轴 - 紧凑布局
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.set_xlim(datetime(2024, 11, 15), datetime(2026, 1, 15))  # 紧凑的x轴范围

# 设置y轴范围，减小空白区域
ax.set_ylim(-0.7, 0.7)

# 隐藏不需要的轴
ax.get_yaxis().set_visible(False)
for spine in ["left", "top", "right"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_position(("data", 0))  # 将x轴置于y=0处

# 优化刻度标签
plt.xticks(rotation=0)
ax.tick_params(axis='x', which='both', length=6, width=1)

# 8. 添加年份标签
ax.text(0.01, -0.15, "2025", transform=ax.transAxes, 
        fontsize=11, fontweight='bold', 
        bbox=dict(boxstyle='round,pad=0.2', fc='lightgray', alpha=0.8))

# 9. 保存为适合LaTeX的PDF
plt.savefig("timeline.pdf", 
            bbox_inches='tight',
            pad_inches=0.05,
            dpi=300)
plt.savefig("timeline.png",  # 同时保存PNG用于预览
            bbox_inches='tight',
            pad_inches=0.05,
            dpi=300)

print("成功生成 timeline.pdf (已优化为LaTeX双栏格式)")