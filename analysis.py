import pandas as pd
import numpy as np
import re
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from dateutil import parser
import warnings

# ==========================================
# 0. 全局画图配置 (针对论文插图优化)
# ==========================================
warnings.filterwarnings("ignore")

# 设置绘图风格
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['axes.unicode_minus'] = False

# 【关键修改】全局字体放大，线条加粗
plt.rcParams.update({
    'font.size': 16,           # 全局默认字体大小
    'axes.labelsize': 18,      # 坐标轴标签大小
    'axes.titlesize': 20,      # 标题大小
    'xtick.labelsize': 14,     # X轴刻度大小
    'ytick.labelsize': 14,     # Y轴刻度大小
    'legend.fontsize': 16,     # 图例大小
    'lines.linewidth': 3.0,    # 线条宽度
    'font.family': ['Arial', 'DejaVu Sans', 'SimHei'] # 字体优先顺序
})

# ==========================================
# 1. 数据加载与清洗
# ==========================================
def load_and_clean_data():
    """加载数据并填充空值"""
    try:
        df_media = pd.read_csv('us_mainstream_media_data.csv')
        df_think = pd.read_csv('us_think_tank_data.csv')
        df_expert = pd.read_csv('us_experts_twitter_data.csv')
    except FileNotFoundError:
        print("错误：找不到CSV文件，请确保文件在当前目录下。")
        return None, None, None
    
    for df in [df_media, df_think, df_expert]:
        df['Content'] = df['Content'].fillna('')
    return df_media, df_think, df_expert

def clean_text(text):
    """基础文本清洗"""
    text = str(text).lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

STOPWORDS = set([
    'the', 'and', 'to', 'of', 'in', 'a', 'is', 'that', 'for', 'on', 'it', 'with', 'as', 
    'are', 'at', 'be', 'this', 'from', 'by', 'have', 'has', 'will', 'an', 'was', 'not', 
    'but', 'we', 'they', 'their', 'which', 'or', 'its', 'about', 'more', 'can', 'us', 
    'new', 'one', 'would', 'also', 'source', 'twitter', 'said', 'image', 'get', 'like',
    'just', 'out', 'up', 'all', 'what', 'so', 'who', 'if', 'when', 'there', 'do', 'no',
    'been', 'year', 'years', 'time', 'other', 'some', 'into', 'over', 'after', 'cnas', 'cset', 'csis',
    'report', 'analysis', 'percent', 'than', 'could', 'may', 'should', 'now', 'even', 'how',
    'click', 'read', 'page', 'loading'
])

def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in STOPWORDS and len(word) > 2])

# ==========================================
# 2. 核心分析函数
# ==========================================

def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

def process_dates(df, date_col):
    """时间清洗：转UTC -> 去时区 -> 过滤2025年"""
    if date_col not in df.columns: return df
    df[date_col] = df[date_col].astype(str)
    # 尝试解析多种日期格式
    df['dt_date'] = pd.to_datetime(df[date_col], utc=True, errors='coerce').dt.tz_localize(None)
    df = df.dropna(subset=['dt_date'])
    df = df[df['dt_date'] >= '2025-01-01']
    return df

def build_advanced_network(df, top_n=30): # 【调整】减少节点数top_n，防止拥挤，从45降到30
    """构建SNA语义网络"""
    if len(df) < 2: return None
    
    cv = CountVectorizer(max_features=top_n, stop_words='english')
    try:
        X = cv.fit_transform(df['processed_text'])
    except ValueError:
        return None
        
    words = cv.get_feature_names_out()
    matrix = (X.T * X)
    matrix.setdiag(0)
    
    G = nx.from_scipy_sparse_array(matrix)
    G = nx.relabel_nodes(G, {i: w for i, w in enumerate(words)})
    
    # 计算中心性和社区
    centrality = nx.degree_centrality(G)
    nx.set_node_attributes(G, centrality, 'centrality')
    
    try:
        communities = nx.community.greedy_modularity_communities(G)
        community_map = {}
        for i, comm in enumerate(communities):
            for node in comm:
                community_map[node] = i
        nx.set_node_attributes(G, community_map, 'community')
    except:
        nx.set_node_attributes(G, 0, 'community')

    return G

# ==========================================
# 3. 执行绘图 (高清大字版)
# ==========================================

print(">>> 正在处理数据...")
df_media, df_think, df_expert = load_and_clean_data()

if df_media is not None:
    # 预处理
    for df in [df_media, df_think, df_expert]:
        df['processed_text'] = df['Content'].apply(clean_text).apply(remove_stopwords)
        df['sentiment'] = df['Content'].apply(get_sentiment)

    df_media = process_dates(df_media, 'Date')
    df_think = process_dates(df_think, 'Date')

    # --- 图表 1: 情感演化趋势 (大字版) ---
    print(">>> 生成图表 1: 情感演化趋势 (sentiment_evolution_2025.pdf)...")
    plt.figure(figsize=(14, 8)) # 【调整】增大画布

    # 重采样处理 (处理报错: 使用ME替代M以兼容新版pandas，或者保持M如果版本旧)
    try:
        media_series = df_media.set_index('dt_date').resample('ME')['sentiment'].mean()
        think_series = df_think.set_index('dt_date').resample('ME')['sentiment'].mean()
    except ValueError:
        media_series = df_media.set_index('dt_date').resample('M')['sentiment'].mean()
        think_series = df_think.set_index('dt_date').resample('M')['sentiment'].mean()

    # 绘图
    plt.plot(media_series.index, media_series.values, marker='o', markersize=10, linestyle='-', linewidth=3.5, label='Media (Public)', color='#d62728') 
    plt.plot(think_series.index, think_series.values, marker='s', markersize=10, linestyle='--', linewidth=3.5, label='Think Tank (Policy)', color='#1f77b4')

    # 设置轴格式
    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator())

    plt.title('Sentiment Evolution Analysis (2025 Monthly)', fontsize=22, fontweight='bold', pad=20)
    plt.ylabel('Sentiment Polarity', fontsize=18)
    plt.xlabel('Date', fontsize=18)
    plt.axhline(0, color='gray', linestyle=':', linewidth=2, alpha=0.7)
    plt.legend(fontsize=16, frameon=True, framealpha=0.9, facecolor='white')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('sentiment_evolution_2025.pdf', dpi=300, format='pdf')

    # --- 图表 2: 专家情感分布 (大字版) ---
    print(">>> 生成图表 2: 专家情感分布 (expert_sentiment_distribution.pdf)...")
    plt.figure(figsize=(12, 8)) # 【调整】增大画布
    sns.histplot(df_expert['sentiment'], kde=True, color='#2ca02c', bins=15, alpha=0.6, edgecolor='white', linewidth=1.5)
    
    mean_val = df_expert['sentiment'].mean()
    plt.axvline(mean_val, color='#d62728', linestyle='--', linewidth=3, label=f"Mean: {mean_val:.2f}")
    
    plt.title('Expert Sentiment Distribution', fontsize=22, fontweight='bold', pad=20)
    plt.xlabel('Sentiment Polarity', fontsize=18)
    plt.ylabel('Frequency', fontsize=18)
    plt.legend(fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('expert_sentiment_distribution.pdf', dpi=300, format='pdf')

    # --- 定义网络绘图函数 (超级大字版) ---
    def draw_professional_network(G, filename, title):
        if not G: return
        # 【关键】设置非常大的画布，保证文字不拥挤
        plt.figure(figsize=(16, 14))
        
        # 【关键】布局算法 k值调大(0.6-0.8)，拉开节点距离
        pos = nx.spring_layout(G, k=0.7, iterations=60, seed=42)
        
        centrality = nx.get_node_attributes(G, 'centrality')
        communities = nx.get_node_attributes(G, 'community')
        weights = [G[u][v]['weight'] for u, v in G.edges()]
        
        # 节点更大
        node_sizes = [v * 12000 + 1000 for v in centrality.values()] 
        node_colors = [communities.get(n, 0) for n in G.nodes()]
        
        # 边更粗
        if weights:
            max_w = max(weights)
            widths = [(w / max_w) * 4 + 0.5 for w in weights]
        else: widths = 2.0

        # 绘制
        nx.draw_networkx_edges(G, pos, width=widths, alpha=0.25, edge_color='#555555')
        # 使用Pastel配色让文字更清晰
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.Pastel1, alpha=0.95, linewidths=2, edgecolors='white')
        
        # 【核心修改】标签超级大，加粗，加背景框
        labels = nx.draw_networkx_labels(G, pos, font_size=18, font_family='sans-serif', font_weight='bold', font_color='#333333')
        
        # 给每个标签加白色半透明背景框，防止被线条干扰
        for _, t in labels.items():
            t.set_bbox(dict(facecolor='white', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.2'))

        plt.title(title, fontsize=24, fontweight='bold', pad=30)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, format='pdf')

    # --- 图表 3 & 4: 生成网络图 ---
    print(">>> 生成图表 3 & 4: 专业语义网络 (高清大字版)...")
    
    # 智库网络
    G_think = build_advanced_network(df_think, top_n=30) # 仅显示Top30词，保证清晰
    draw_professional_network(G_think, 'network_think_tank_pro.pdf', 'Think Tank Semantic Network')

    # 专家网络
    G_expert = build_advanced_network(df_expert, top_n=35) # 专家词汇较散，稍微多一点
    draw_professional_network(G_expert, 'network_expert_pro.pdf', 'Expert Semantic Network')

    print("\n>>> 全部完成！生成的PDF图表已优化字体大小，可直接插入LaTeX。")
else:
    print("无法运行绘图，请检查数据文件。")