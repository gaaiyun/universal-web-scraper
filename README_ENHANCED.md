# Universal Web Scraper

**通用网页爬虫框架**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 项目概述

Universal Web Scraper 是一个**通用网页爬虫框架**，支持多种网站类型的结构化数据提取。适用于数据采集、市场分析、竞品监控等场景。

**核心特点**：
- **多适配器** - 新闻/电商/招聘/博客网站
- **结构化输出** - CSV/JSON/Excel
- **Streamlit UI** - 交互式爬虫界面
- **可扩展** - 轻松添加新适配器
- **批量爬取** - 支持多页面并发

---

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 基础使用

```python
from scripts.scraper import UniversalScraper

scraper = UniversalScraper()
data = scraper.scrape('https://example.com', adapter='generic')
print(data)
```

### 运行 Dashboard

```bash
streamlit run dashboard.py
```

访问 http://localhost:8501

---

## 项目结构

```
Universal-Web-Scraper/
├── adapters/              # 网站适配器
│   ├── base.py           # 基础适配器
│   ├── news.py           # 新闻网站
│   ├── ecommerce.py      # 电商网站
│   ├── job.py            # 招聘网站
│   └── generic.py        # 通用适配器
├── scripts/              # 爬虫脚本
│   ├── scraper.py        # 主爬虫
│   ├── batch_scraper.py  # 批量爬取
│   └── data_cleaner.py   # 数据清洗
├── templates/            # 高级模板
│   └── advanced_templates.py
├── dashboard.py          # Streamlit 界面
├── requirements.txt      # 依赖
└── README.md             # 本文档
```

---

## 使用场景

| 场景 | 适配器 | 输出字段 |
|------|--------|----------|
| 新闻监控 | news | 标题、摘要、日期、作者 |
| 电商比价 | ecommerce | 商品名、价格、评分、图片 |
| 职位搜索 | job | 职位、公司、地点、薪资 |
| 博客采集 | generic | 标题、内容、标签、链接 |

---

## 高级功能

### 1. 批量爬取

```python
from scripts.batch_scraper import BatchScraper

scraper = BatchScraper()
urls = ['url1.com', 'url2.com', 'url3.com']
results = scraper.scrape_all(urls, max_workers=5)
```

### 2. 数据清洗

```python
from scripts.data_cleaner import DataCleaner

cleaner = DataCleaner()
clean_data = cleaner.clean(raw_data, remove_duplicates=True)
```

### 3. 自定义适配器

```python
from adapters.base import BaseAdapter

class CustomAdapter(BaseAdapter):
    def parse(self, html):
        # 自定义解析逻辑
        pass
```

---

## Streamlit Dashboard

### 功能
- URL 输入配置
- 实时爬取预览
- 统计信息展示
- 多格式导出（CSV/JSON/Excel）

### 截图
运行 `streamlit run dashboard.py` 查看

---

## 注意事项

1. **遵守 robots.txt** - 尊重网站爬虫协议
2. **请求频率** - 添加延迟，避免被封
3. **用户代理** - 使用合理的 User-Agent
4. **数据使用** - 遵守网站服务条款

---

## 相关资源

- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests 文档](https://docs.python-requests.org/)
- [Streamlit 文档](https://docs.streamlit.io/)

---

## 更新日志

### 2026-03-02
- 添加 Streamlit Dashboard
- 添加高级爬虫模板
- 支持 4 种网站类型

---

_最后更新：2026-03-02_
