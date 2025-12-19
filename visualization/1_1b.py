import matplotlib.pyplot as plt
import numpy as np

# 1. 准备数据
years = ['2018', '2020', '2022', '2024', '2025(Proj)']
counts = [130, 260, 500, 855, 2000]
total_list_est = [1100, 1650, 2500, 3200, 4500]
proportions = [(c / t) * 100 for c, t in zip(counts, total_list_est)]

# 2. 设置LaTeX友好风格 - 增大字体
plt.rcParams.update({
    'font.sans-serif': ['SimHei', 'Arial', 'DejaVu Sans'],
    'axes.unicode_minus': False,
    'font.size': 11,  # 基础字体增大
    'axes.titlesize': 13,
    'axes.labelsize': 12,  # 坐标轴标签字体增大
    'xtick.labelsize': 11,  # x轴刻度字体增大
    'ytick.labelsize': 11,  # y轴刻度字体增大
    'legend.fontsize': 10,
    'figure.constrained_layout.use': True,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.linewidth': 1.2,  # 加粗坐标轴线
})

# 3. 创建适合LaTeX双栏的宽矮图形
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.5),  # 宽度大，高度小
                               gridspec_kw={'wspace': 0.3, 'width_ratios': [1, 1]})

# 创建渐变颜色 - 从浅蓝到深蓝
colors = plt.cm.Blues(np.linspace(0.5, 0.9, len(counts)))

# --- 左图：渐变柱状图 (数量增长) ---
bars = ax1.bar(years, counts, color=colors, width=0.7, 
               edgecolor='darkblue', linewidth=1.5, zorder=3)

# 添加数值标签 - 增大字体
for bar in bars:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h + 60, 
             f'{int(h)}', 
             ha='center', 
             fontsize=11,  # 增大数值标签字体
             fontweight='bold',
             color='darkblue')

ax1.set_title('BIS实体清单：中国半导体/高科技企业数量', 
              fontsize=13, fontweight='bold', pad=12)
ax1.set_ylabel('企业数量 (家)', fontsize=12, fontweight='bold', labelpad=10)
ax1.set_xlabel('年份', fontsize=12, fontweight='bold', labelpad=8)

# 设置网格和y轴范围
ax1.grid(axis='y', linestyle='--', alpha=0.6, zorder=0)
ax1.set_ylim(0, 2200)
ax1.set_yticks(np.arange(0, 2201, 400))

# 美化坐标轴
ax1.tick_params(axis='both', which='major', labelsize=11, length=6, width=1.5)

# --- 右图：美化折线图 (占比增长) ---
# 使用渐变色点
marker_colors = plt.cm.Reds(np.linspace(0.6, 0.9, len(proportions)))

line = ax2.plot(years, proportions, marker='o', 
                color='#d63031', linewidth=3.5, 
                markersize=10, markeredgecolor='white',
                markeredgewidth=1.5, zorder=3)

# 添加百分比标签 - 增大字体
for i, (year, val, color) in enumerate(zip(years, proportions, marker_colors)):
    ax2.annotate(f'{val:.1f}%', 
                 (year, proportions[i]), 
                 textcoords="offset points", 
                 xytext=(0, 12),  # 略微增加偏移
                 ha='center', 
                 fontsize=11,  # 增大百分比标签字体
                 fontweight='bold',
                 color='#b71540',
                 bbox=dict(boxstyle='round,pad=0.2', 
                          facecolor='white', 
                          edgecolor='lightgray', 
                          alpha=0.8))

ax2.set_title('中国半导体企业在BIS总清单中的占比演变', 
              fontsize=13, fontweight='bold', pad=12)
ax2.set_ylabel('占比 (%)', fontsize=12, fontweight='bold', labelpad=10)
ax2.set_xlabel('年份', fontsize=12, fontweight='bold', labelpad=8)

# 设置网格和y轴范围
ax2.grid(True, linestyle='--', alpha=0.6, zorder=0)
ax2.set_ylim(0, 65)
ax2.set_yticks(np.arange(0, 66, 10))

# 美化坐标轴
ax2.tick_params(axis='both', which='major', labelsize=11, length=6, width=1.5)

# 添加趋势线注解
ax2.text(0.02, 0.98, '增长趋势', 
         transform=ax2.transAxes,
         fontsize=10,
         fontstyle='italic',
         color='#d63031',
         verticalalignment='top',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='lightgray', alpha=0.7))

# 4. 调整整体布局
plt.tight_layout(pad=2.0, h_pad=1.5, w_pad=2.0)

# 5. 保存为适合LaTeX的PDF
plt.savefig('bis_combined_analysis.pdf', 
            bbox_inches='tight',
            pad_inches=0.08,
            dpi=300)

plt.savefig('bis_combined_analysis.png',  # 同时保存PNG用于预览
            bbox_inches='tight',
            pad_inches=0.08,
            dpi=300)

print("成功生成 bis_combined_analysis.pdf (已优化为LaTeX双栏格式)")
plt.show()