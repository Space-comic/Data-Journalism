import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# 中文字体设置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

quarters = ['2023 Q3', '2024 Q1', '2024 Q3', '2025 Q1', '2025 Q3(预估)']
total_rev = [18.1, 26.0, 35.1, 38.0, 42.0]  # 全球总营收
china_share = [22, 18, 12, 9, 8]             # 中国区占比

fig, ax1 = plt.subplots(figsize=(12, 5))

# 绘制带有渐变效果的柱状图
for i, val in enumerate(total_rev):
    grad = np.atleast_2d(np.linspace(0, 1, 256)).T
    ax1.imshow(grad, extent=[i-0.3, i+0.3, 0, val], aspect='auto', 
               cmap=mcolors.LinearSegmentedColormap.from_list('rev_grad', ['#d1d8e0', '#2c3e50']), zorder=1)

ax1.set_xlim(-0.5, len(quarters)-0.5)
ax1.set_ylim(0, 50)
ax1.set_ylabel('全球总营收 (十亿美元)', color='#2c3e50', fontsize=11, fontweight='bold')
ax1.set_xticks(range(len(quarters)))
ax1.set_xticklabels(quarters, fontweight='bold')

# 绘制中国区占比折线 (高亮红)
ax2 = ax1.twinx()
ax2.plot(range(len(quarters)), china_share, color='#ff4757', marker='o', linewidth=4, markersize=10, zorder=5)
ax2.fill_between(range(len(quarters)), china_share, color='#ff4757', alpha=0.1) # 增加淡红色阴影
ax2.set_ylabel('中国区占比 (%)', color='#ff4757', fontsize=11, fontweight='bold')
ax2.set_ylim(0, 30)

# 标注数值
for i, txt in enumerate(china_share):
    ax2.annotate(f'{txt}%', (i, china_share[i]), textcoords="offset points", xytext=(0, 12), ha='center', color='#e84118', fontweight='bold')
plt.savefig("3_4b.pdf", bbox_inches='tight')