import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- 关键：中文字体全局设置 ---
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'sans-serif'] # 优先黑体
plt.rcParams['axes.unicode_minus'] = False # 解决负号显示问题

# 1. 创建画布：极扁平比例 (14:3.5)
fig, ax = plt.subplots(figsize=(14, 3.5))
ax.set_xlim(0, 14)
ax.set_ylim(0, 3.5)

# 2. 定义配色
color_main = '#2c3e50'  # 深灰蓝
color_algo = '#3498db'  # 算法蓝

# 3. 绘制节点函数
def draw_box(x, y, text, width=2.4, height=1.1, is_algo=False):
    facecolor = 'white' if not is_algo else '#ecf0f1'
    edgecolor = color_main if not is_algo else color_algo
    rect = patches.FancyBboxPatch((x-width/2, y-height/2), width, height,
                                  boxstyle="round,pad=0.1", linewidth=1.5,
                                  edgecolor=edgecolor, facecolor=facecolor)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center', fontsize=18, fontweight='bold', color=color_main)

# 4. 放置各个阶段节点 (基于论文数据)
# 输入层 [cite: 53, 54, 55]
draw_box(1.5, 1.75, "多源异构语料\n(82份智库/79篇新闻)\n(59条专家评论)") 

# 预处理层 [cite: 182]
draw_box(4.5, 1.75, "文本预处理\n& 特征量化\n(TF-IDF算法)")

# 核心算法层 [cite: 194, 199, 204]
draw_box(7.5, 2.7, "LDA主题聚类\n(潜在议题挖掘)", width=2.2, height=0.7, is_algo=True)
draw_box(7.5, 1.75, "情感演化计算\n(动态态势量化)", width=2.2, height=0.7, is_algo=True)
draw_box(7.5, 0.8, "SNA语义网络\n(认知拓扑分析)", width=2.2, height=0.7, is_algo=True)

# 输出层 [cite: 212]
draw_box(11.5, 1.75, "多维对抗态势结论\n(战略/舆论/技术视角)\n[实证研判]")

# 5. 绘制箭头
arrow_style = dict(arrowstyle='-|>', color=color_main, linewidth=1.5, mutation_scale=20)
ax.annotate('', xy=(3.2, 1.75), xytext=(2.8, 1.75), arrowprops=arrow_style)
ax.annotate('', xy=(6.3, 1.75), xytext=(5.8, 1.75), arrowprops=arrow_style)

for y_pos in [2.7, 1.75, 0.8]:
    ax.annotate('', xy=(10.2, 1.75), xytext=(8.7, y_pos), 
                arrowprops=dict(arrowstyle='-|>', color=color_algo, linewidth=1, alpha=0.6))

# 6. 保存与显示
ax.axis('off')
plt.tight_layout()
plt.savefig("2_4.pdf", bbox_inches='tight') 