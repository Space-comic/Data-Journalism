import os
import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
from curl_cffi import requests as cffi_requests  # 专门用于 Politico

# --- 配置 ---
INPUT_FILE = 'data_urls.txt'
OUTPUT_THINK_TANK = 'us_think_tank_data.csv'
OUTPUT_MEDIA = 'us_mainstream_media_data.csv'

# 定义分组
THINK_TANKS = ['CNAS', 'CSET', 'CSIS']
MEDIA = ['Politico', 'VOA News']

# 通用请求头
COMMON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}

def get_source_name(url):
    """根据URL判断来源"""
    if 'cnas.org' in url: return 'CNAS'
    if 'cset.georgetown.edu' in url: return 'CSET'
    if 'csis.org' in url: return 'CSIS'
    if 'politico.com' in url: return 'Politico'
    if 'voanews.com' in url: return 'VOA News'
    return 'Unknown'

# ============================
# 1. 核心抓取函数 (网络层)
# ============================

def fetch_content_requests(url):
    """通用抓取 (CNAS, CSET, CSIS, VOA)"""
    try:
        time.sleep(random.uniform(1, 3)) # 随机延时
        response = requests.get(url, headers=COMMON_HEADERS, timeout=20)
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
    except Exception as e:
        print(f"   [Error] 普通抓取失败 {url}: {e}")
        return None

def fetch_content_cffi(url):
    """特殊抓取 (Politico) - 使用 curl_cffi 模拟真实浏览器"""
    try:
        time.sleep(random.uniform(2, 4))
        # 模拟 Chrome 120
        response = cffi_requests.get(url, impersonate="chrome120", timeout=30)
        if response.status_code != 200:
            print(f"   [Error] CFFI status {response.status_code}")
            return None
        return response.text
    except Exception as e:
        print(f"   [Error] CFFI抓取失败 {url}: {e}")
        return None

# ============================
# 2. 解析逻辑 (根据你提供的脚本移植)
# ============================

def parse_cnas(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else ''
    
    # 尝试多种日期格式
    date_text = ''
    time_tag = soup.find('time')
    if time_tag:
        date_text = time_tag.get_text(strip=True)
    
    # CNAS 正文提取逻辑
    content = ''
    wrapper = soup.find('div', class_='wysiwyg-wrapper') # 原脚本逻辑
    if wrapper:
        content = wrapper.get_text(separator='\n', strip=True)
    else:
        # Fallback
        paragraphs = soup.find_all('p')
        content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        
    return {'Title': title, 'Date': date_text, 'URL': url, 'Content': content}

def parse_cset(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    
    title = ''
    header = soup.find('header', class_='article-header')
    if header and header.find('h1'):
        title = header.find('h1').get_text(strip=True)
    elif soup.find('h1', class_='entry-title'):
        title = soup.find('h1', class_='entry-title').get_text(strip=True)
        
    date_text = ''
    if header and header.find('div', class_='meta-date'):
         date_text = header.find('div', class_='meta-date').get_text(strip=True)

    # CSET 正文提取逻辑
    content_div = soup.find('div', class_='entry-content')
    content = content_div.get_text(separator='\n', strip=True) if content_div else ''
    
    return {'Title': title, 'Date': date_text, 'URL': url, 'Content': content}

def parse_csis(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.find('h1').get_text(strip=True) if soup.find('h1') else ''
    date_text = soup.find('p', class_='date').get_text(strip=True) if soup.find('p', class_='date') else ''
    
    # CSIS 正文提取逻辑 (原脚本逻辑)
    paragraphs_list = []
    # 优先找 wysiwyg-wrapper
    text_wrappers = soup.find_all('div', class_='wysiwyg-wrapper')
    if text_wrappers:
        for wrapper in text_wrappers:
            ps = wrapper.find_all('p')
            for p in ps:
                txt = p.get_text(strip=True)
                if txt: paragraphs_list.append(txt)
    else:
        # Fallback to text-block
        text_blocks = soup.find_all('div', attrs={'data-block-plugin-id': 'text-block'})
        for block in text_blocks:
            ps = block.find_all('p')
            for p in ps:
                paragraphs_list.append(p.get_text(strip=True))
                
    content = '\n\n'.join(paragraphs_list)
    return {'Title': title, 'Date': date_text, 'URL': url, 'Content': content}

def parse_politico(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    
    title = ''
    h1 = soup.find('h1')
    if h1: title = h1.get_text(strip=True)
    
    date_text = ''
    time_tag = soup.find('time')
    if time_tag and time_tag.has_attr('datetime'):
        date_text = time_tag['datetime']
        
    # Politico 正文提取逻辑 (原脚本逻辑)
    content_list = []
    paragraphs = soup.find_all('p', class_='story-text__paragraph')
    for p in paragraphs:
        content_list.append(p.get_text(strip=True))
    
    content = '\n\n'.join(content_list)
    return {'Title': title, 'Date': date_text, 'URL': url, 'Content': content}

def parse_voa(html, url):
    soup = BeautifulSoup(html, 'html.parser')
    
    title = ''
    h1 = soup.find('h1', class_='title')
    if h1: title = h1.get_text(strip=True)
    
    date_text = ''
    time_tag = soup.find('time')
    if time_tag: date_text = time_tag.get_text(strip=True)
    
    # VOA 正文提取逻辑 (原脚本逻辑)
    content = ''
    article_body = soup.find('div', id='article-content')
    if article_body:
        content = article_body.get_text(separator='\n', strip=True)
        
    return {'Title': title, 'Date': date_text, 'URL': url, 'Content': content}

# ============================
# 3. 主程序
# ============================

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"错误: 找不到 {INPUT_FILE}")
        return

    # 读取链接
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"总共找到 {len(urls)} 个链接，开始处理...")
    
    all_data = []

    for idx, url in enumerate(urls):
        source = get_source_name(url)
        print(f"[{idx+1}/{len(urls)}] 处理 [{source}]: {url}")
        
        # 1. 抓取 HTML
        html = None
        if source == 'Politico':
            html = fetch_content_cffi(url)
        elif source in ['CNAS', 'CSET', 'CSIS', 'VOA News']:
            html = fetch_content_requests(url)
        else:
            print(f"   [Skip] 未知来源域名")
            continue
            
        if not html:
            continue

        # 2. 解析 HTML
        try:
            row_data = {}
            if source == 'CNAS': row_data = parse_cnas(html, url)
            elif source == 'CSET': row_data = parse_cset(html, url)
            elif source == 'CSIS': row_data = parse_csis(html, url)
            elif source == 'Politico': row_data = parse_politico(html, url)
            elif source == 'VOA News': row_data = parse_voa(html, url)
            
            # 3. 添加来源列
            if row_data:
                row_data['来源'] = source
                # 简单清洗数据：如果内容太短，可能是失败
                if len(row_data.get('Content', '')) < 20:
                    print(f"   [Warn] 内容为空或过短")
                
                all_data.append(row_data)
                print(f"   -> 成功提取: {row_data.get('Title', '')[:20]}...")
                
        except Exception as e:
            print(f"   [Error] 解析出错: {e}")

    # ============================
    # 4. 数据整合与导出
    # ============================
    
    if not all_data:
        print("未抓取到任何数据。")
        return

    df = pd.DataFrame(all_data)
    
    # 确保列顺序，把'来源'放在第一位
    cols = ['来源', 'Title', 'Date', 'URL', 'Content']
    # 可能会有一些额外的列不存在，做个交集处理
    final_cols = [c for c in cols if c in df.columns]
    df = df[final_cols]

    # 分割数据
    df_think_tank = df[df['来源'].isin(THINK_TANKS)]
    df_media = df[df['来源'].isin(MEDIA)]

    # 保存
    if not df_think_tank.empty:
        df_think_tank.to_csv(OUTPUT_THINK_TANK, index=False, encoding='utf-8-sig')
        print(f"\n成功生成美方智库数据: {OUTPUT_THINK_TANK} (包含 {len(df_think_tank)} 条)")
    
    if not df_media.empty:
        df_media.to_csv(OUTPUT_MEDIA, index=False, encoding='utf-8-sig')
        print(f"成功生成美方媒体数据: {OUTPUT_MEDIA} (包含 {len(df_media)} 条)")

if __name__ == "__main__":
    main()