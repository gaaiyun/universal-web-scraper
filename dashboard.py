"""
Universal Web Scraper - Streamlit Dashboard
交互式网页爬虫界面
"""

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time


# 页面配置
st.set_page_config(
    page_title="Universal Web Scraper",
    page_icon="🕷️",
    layout="wide"
)

# 标题
st.title("🕷️ Universal Web Scraper Dashboard")
st.markdown("---")

# 侧边栏
st.sidebar.header("⚙️ 爬虫配置")

# 选择爬虫类型
scraper_type = st.sidebar.selectbox(
    "选择爬虫类型",
    ["通用网页", "新闻网站", "电商网站", "招聘网站", "自定义"]
)

# URL 输入
url = st.sidebar.text_input(
    "输入 URL",
    "https://example.com"
)

# 爬取选项
st.sidebar.subheader("选项")
extract_links = st.sidebar.checkbox("提取链接", value=True)
extract_images = st.sidebar.checkbox("提取图片", value=False)
extract_text = st.sidebar.checkbox("提取正文", value=True)
max_pages = st.sidebar.slider("最大页数", 1, 100, 5)

# 开始按钮
if st.sidebar.button("🚀 开始爬取", type="primary"):
    st.sidebar.success("爬取开始！")
    
    # 模拟爬取过程
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    
    for i in range(100):
        time.sleep(0.05)
        progress_bar.progress(i + 1)
        status_text.text(f"爬取中... {i+1}%")
    
    status_text.text("✅ 爬取完成！")

# 主界面
tab1, tab2, tab3, tab4 = st.tabs(["📊 结果预览", "📝 原始数据", "📈 统计信息", "💾 导出"])

# Tab 1: 结果预览
with tab1:
    st.header("📊 爬取结果预览")
    
    # 模拟数据
    sample_data = {
        '标题': ['示例文章 1', '示例文章 2', '示例文章 3', '示例文章 4', '示例文章 5'],
        'URL': [
            'https://example.com/article/1',
            'https://example.com/article/2',
            'https://example.com/article/3',
            'https://example.com/article/4',
            'https://example.com/article/5'
        ],
        '发布日期': pd.date_range(start='2024-01-01', periods=5),
        '作者': ['作者 A', '作者 B', '作者 A', '作者 C', '作者 B'],
        '字数': [1200, 800, 1500, 950, 1100]
    }
    
    df = pd.DataFrame(sample_data)
    st.dataframe(df, use_container_width=True)
    
    # 搜索结果
    st.subheader("🔍 搜索")
    search_query = st.text_input("搜索关键词")
    if search_query:
        filtered = df[df['标题'].str.contains(search_query, case=False)]
        st.write(f"找到 {len(filtered)} 条结果")
        st.dataframe(filtered, use_container_width=True)

# Tab 2: 原始数据
with tab2:
    st.header("📝 原始 HTML 数据")
    
    sample_html = """
    <html>
        <head><title>示例页面</title></head>
        <body>
            <h1>欢迎访问示例网站</h1>
            <article>
                <h2>文章标题 1</h2>
                <p>这是文章内容...</p>
            </article>
        </body>
    </html>
    """
    
    st.code(sample_html, language="html")
    
    st.subheader("解析后的文本")
    st.text("欢迎访问示例网站\n文章标题 1\n这是文章内容...")

# Tab 3: 统计信息
with tab3:
    st.header("📈 爬取统计")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总页面数", "5", "+2")
    
    with col2:
        st.metric("总链接数", "127", "+15")
    
    with col3:
        st.metric("总图片数", "43", "+8")
    
    with col4:
        st.metric("总字数", "5,550", "+1,200")
    
    st.markdown("---")
    
    # 图表
    st.subheader("数据分布")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 作者分布
        author_counts = df['作者'].value_counts()
        st.bar_chart(author_counts)
    
    with col2:
        # 字数分布
        st.histogram(df['字数'], bin_count=10)

# Tab 4: 导出
with tab4:
    st.header("💾 导出数据")
    
    st.subheader("选择导出格式")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 导出 CSV", use_container_width=True):
            st.success("CSV 文件已生成！")
            st.download_button(
                label="⬇️ 下载 CSV",
                data=df.to_csv(index=False),
                file_name=f"scraper_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 导出 Excel", use_container_width=True):
            st.success("Excel 文件已生成！")
            st.download_button(
                label="⬇️ 下载 Excel",
                data=df.to_csv(index=False),
                file_name=f"scraper_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col3:
        if st.button("📋 导出 JSON", use_container_width=True):
            st.success("JSON 文件已生成！")
            st.download_button(
                label="⬇️ 下载 JSON",
                data=df.to_json(orient='records'),
                file_name=f"scraper_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    st.markdown("---")
    
    st.subheader("导出选项")
    st.checkbox("包含原始 HTML")
    st.checkbox("包含图片 URL")
    st.checkbox("包含元数据")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Universal Web Scraper | Powered by Streamlit</p>
    <p>📝 支持：通用网页 | 新闻网站 | 电商网站 | 招聘网站</p>
</div>
""", unsafe_allow_html=True)
