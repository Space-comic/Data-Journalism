import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# 设置绘图风格
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# --- 数据准备 ---
companies = ['Nvidia', 'Intel', 'AMD', 'Applied Materials', 'Lam Research']
revenue_before = [25, 36, 32, 35, 31]
revenue_now = [17, 24, 22, 28, 26]

df_rev = pd.DataFrame({
    'Company': companies,
    'Before': revenue_before,
    'Now': revenue_now
})

tech_fields = ['Logic (GPU/CPU)', 'Memory (DRAM)', 'Stacking', 'AI/LLM']
policy_intensity = ['Low Intensity', 'Trade Friction', 'EAR Controls', 'Entity List']
heatmap_data = np.array([
    [20, 40, 60, 85],
    [30, 50, 75, 40],
    [15, 35, 80, 95],
    [10, 25, 70, 98]
])

# --- 创建画布 ---
# 稍微减小整体 figsize 宽度，避免在双栏中显得过度拉伸
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=300)

# 1. 绘制上方图 (Bar Chart)
y_pos = np.arange(len(companies))
width = 0.35
color_before, color_now = '#2c3e50', '#e74c3c'

ax1.barh(y_pos - width/2, df_rev['Before'], width, label='Pre-Sanctions (2023/24)', color=color_before, alpha=0.85)
ax1.barh(y_pos + width/2, df_rev['Now'], width, label='Post-Sanctions (2025E)', color=color_now, alpha=0.85)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(companies, fontsize=12)
ax1.set_xlabel('Revenue Share (%)', fontsize=13)
ax1.set_title('(a):美方半导体巨头对华依赖度变化', fontsize=15, pad=15, fontweight='bold')
ax1.legend(fontsize=11, loc='upper right')
ax1.grid(axis='x', linestyle='--', alpha=0.5)

# 【关键步骤】手动调整第一张图的尺寸 (横向长度减少)
# set_position([左边界, 下边界, 宽度, 高度])
# 这里的 0.2 和 0.6 表示将宽度从原来的约 0.8 缩小到 0.6，并向右偏移 0.2 以居中
ax1.set_position([0.15, 0.6, 0.6, 0.32]) 

# 2. 绘制下方图 (Heatmap)
# 第二张图保持较宽的尺寸以展示复杂矩阵
sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", 
            xticklabels=policy_intensity, yticklabels=tech_fields, 
            ax=ax2, cbar_kws={'label': 'Expert Focus Intensity', 'shrink': 0.8},
            annot_kws={"size": 13, "weight": "bold"})

ax2.set_title('(b):制裁压力下的技术突围热力分布', fontsize=15, pad=15, fontweight='bold')
ax2.set_xlabel('Policy Intensity', fontsize=13)
ax2.set_ylabel('Core Tech Fields', fontsize=13)
ax2.tick_params(axis='both', which='major', labelsize=11)

# 手动调整第二张图的尺寸，使其横向铺满
ax2.set_position([0.15, 0.1, 0.6, 0.35])

# 注意：使用了 set_position 后不要使用 tight_layout，否则会自动重置位置
# plt.tight_layout() 

# 保存为 PDF
output_file = '3_4.pdf'
plt.savefig(output_file, bbox_inches='tight')
print(f"图表已保存为: {output_file}")