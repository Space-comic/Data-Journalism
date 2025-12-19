import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# --- 全局设置 ---
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 数据准备 - 图3.6a (情感矩阵)
summary_data = {
    'Source': ['主流媒体', '核心智库', '技术专家', '社交媒体', '官方声明'],
    'Mean_Sentiment': [-0.25, 0.08, 0.15, -0.12, 0.02],
    'Volatility': [0.45, 0.05, 0.18, 0.38, 0.12],
    'Topic_Coverage': [90, 75, 85, 60, 50]
}
df_summary = pd.DataFrame(summary_data)

# 2. 数据准备 - 图3.6b (雷达图)
labels = ['政治敏感度', '技术深度', '情感烈度', '制度严密性', '市场关联度']
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

stats_thinktank = [8, 6, 2, 9, 5, 8]
stats_media = [9, 3, 9, 4, 7, 9]
stats_expert = [3, 9, 4, 6, 9, 3]

# --- 创建画布 ---
# figsize=(20, 8) 确保了宽屏比例，纵向高度减小
fig = plt.figure(figsize=(20, 8), dpi=300)

# ==========================================
# 子图 1: 情感分布矩阵 (左侧)
# ==========================================
ax1 = fig.add_subplot(1, 2, 1)

# 使用更丰富的颜色序列
vivid_colors = ['#FF1493', '#1E90FF', '#32CD32', '#FFA500', '#8A2BE2']
scatter = ax1.scatter(df_summary['Mean_Sentiment'], 
                     df_summary['Volatility'], 
                     s=df_summary['Topic_Coverage'] * 35, # 加大坐标点
                     c=vivid_colors, 
                     alpha=0.7, 
                     edgecolors='black', 
                     linewidth=2)

# 添加标签并加大字体
for i, txt in enumerate(df_summary['Source']):
    ax1.annotate(txt, (df_summary['Mean_Sentiment'][i], df_summary['Volatility'][i]), 
                xytext=(0, 15), textcoords='offset points', ha='center', 
                fontsize=16, weight='bold')

# 辅助线与区域填充
ax1.axvline(0, color='black', linestyle='--', alpha=0.3)
ax1.set_xlabel('情感均值 (偏负面 <--- 0 ---> 偏正面)', fontsize=18, fontweight='bold')
ax1.set_ylabel('情绪波动率 (受新闻驱动程度)', fontsize=18, fontweight='bold')
ax1.set_title('(a):美方主体情感定力与倾向矩阵', fontsize=22, pad=25, weight='bold')

# 加大刻度字体
ax1.tick_params(axis='both', labelsize=15)

# 区域说明文字加大
ax1.fill_between([-0.5, 0], 0.25, 0.5, color='red', alpha=0.08)
ax1.text(-0.35, 0.42, '舆论动员区', color='#c0392b', fontsize=16, weight='bold')
ax1.fill_between([0, 0.5], 0, 0.2, color='green', alpha=0.08)
ax1.text(0.3, 0.1, '技术理性区', color='#27ae60', fontsize=16, weight='bold')

ax1.grid(True, linestyle=':', alpha=0.6)

# ==========================================
# 子图 2: 认知镜像雷达图 (右侧)
# ==========================================
ax2 = fig.add_subplot(1, 2, 2, polar=True)

# 绘制数据
ax2.plot(angles, stats_thinktank, color='#0047AB', linewidth=4, label='智库视角 (战略补漏)')
ax2.fill(angles, stats_thinktank, color='#0047AB', alpha=0.3)

ax2.plot(angles, stats_media, color='#E31A1C', linewidth=4, label='媒体视角 (舆论动员)')
ax2.fill(angles, stats_media, color='#E31A1C', alpha=0.25)

ax2.plot(angles, stats_expert, color='#33A02C', linewidth=4, label='专家视角 (技术现实)')
ax2.fill(angles, stats_expert, color='#33A02C', alpha=0.2)

# 设置雷达图坐标轴与字体
ax2.set_theta_offset(np.pi / 2)
ax2.set_theta_direction(-1)

# 加大雷达图标签字体
ax2.set_thetagrids(np.degrees(angles[:-1]), labels, fontsize=16, fontweight='bold')

# 设置纵轴范围与刻度
ax2.set_ylim(0, 10)
ax2.tick_params(labelsize=14) 

# 加大图例并调整位置
ax2.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=15, frameon=True)

ax2.set_title('(b):中美芯片对抗三方主体画像', fontsize=22, pad=40, weight='bold', color='#2c3e50')

# --- 最终输出控制 ---
plt.tight_layout(pad=4.0) # 增加间距防止左右重叠
output_pdf = "3_5.pdf"
plt.savefig(output_pdf, bbox_inches='tight')
plt.show()

print(f"合并后的PDF图表已生成: {output_pdf}")