> **维护状态说明**：本仓库当前是 AI 辅助生成的初始脚手架，未在生产环境持续打磨。代码可作为参考与起点，使用前请自行核对接口、依赖与边界条件。如果你打算接手维护、把它合并到其他项目，或者发现 bug，欢迎开 issue 或 PR。
# Universal Web Scraper Skill

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**通用网页爬虫 OpenClaw Skill - 展示数据爬取和处理能力**

基于 Scrapling 和 Crawlee-Python 的通用爬虫框架，支持多站点数据采集、智能反爬虫、数据清洗和多格式导出。

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd C:\Users\gaaiy\.openclaw\workspace\skills\universal-web-scraper
pip install scrapling crawlee beautifulsoup4 pandas playwright
playwright install
```

### 2. 基础使用

```bash
# 爬取单个页面
python scripts/scrape.py --url "https://example.com" --output data.json

# 爬取多个页面
python scripts/scrape.py --urls urls.txt --output results.csv

# 使用适配器爬取特定网站
python scripts/scrape.py --adapter ecommerce --url "https://shop.example.com"
```

---

## 📖 功能特性

### 智能爬虫引擎
- ✅ **自适应解析** - 网站结构变化自动适配
- ✅ **智能反爬虫** - 绕过 Cloudflare、验证码
- ✅ **代理轮换** - 自动代理池管理
- ✅ **并发爬取** - 高效多线程/异步

### 多站点支持
- ✅ **电商平台** - 商品信息、价格监控
- ✅ **招聘网站** - 职位数据、薪资分析
- ✅ **新闻媒体** - 文章采集、舆情监控
- ✅ **社交媒体** - 用户数据、评论分析

### 数据处理
- ✅ **数据清洗** - 去重、格式化、验证
- ✅ **数据转换** - 结构化处理
- ✅ **多格式导出** - CSV, JSON, Excel, Database
- ✅ **增量更新** - 只爬取新数据

---

## 📝 使用示例

### 示例 1: 爬取电商商品

```python
from universal_scraper import UniversalScraper

scraper = UniversalScraper(adapter='ecommerce')
products = scraper.scrape('https://shop.example.com/products')

for product in products:
    print(f"{product['title']}: ${product['price']}")
```

### 示例 2: 招聘数据采集

```python
from universal_scraper import UniversalScraper

scraper = UniversalScraper(adapter='job')
jobs = scraper.scrape('https://jobs.example.com/search?q=python')

# 导出为 CSV
scraper.export(jobs, 'jobs.csv', format='csv')
```

### 示例 3: 批量爬取

```python
from universal_scraper import BatchScraper

urls = [
    'https://example1.com',
    'https://example2.com',
    'https://example3.com'
]

scraper = BatchScraper(max_workers=5)
results = scraper.scrape_batch(urls)
```

---

## ⚙️ 配置说明

### 配置文件 (config/default.yaml)

```yaml
scraper:
  user_agent: "Mozilla/5.0 ..."
  timeout: 30
  retry: 3
  delay: 1.0

proxy:
  enabled: true
  rotation: true
  pool_size: 10

output:
  format: json
  encoding: utf-8
  clean: true
```

### 环境变量

```bash
# 代理配置
PROXY_URL=http://proxy.example.com:8080
PROXY_USERNAME=user
PROXY_PASSWORD=pass

# 数据库配置（可选）
DATABASE_URL=postgresql://user:pass@localhost/scraper
```

---

## 🎯 适配器列表

### 1. 电商适配器 (ecommerce)
```python
scraper = UniversalScraper(adapter='ecommerce')
products = scraper.scrape(url)
# 返回: title, price, image, description, rating
```

### 2. 招聘适配器 (job)
```python
scraper = UniversalScraper(adapter='job')
jobs = scraper.scrape(url)
# 返回: title, company, salary, location, requirements
```

### 3. 新闻适配器 (news)
```python
scraper = UniversalScraper(adapter='news')
articles = scraper.scrape(url)
# 返回: title, author, date, content, tags
```

### 4. 通用适配器 (generic)
```python
scraper = UniversalScraper(adapter='generic')
data = scraper.scrape(url, selectors={'title': 'h1', 'content': '.article'})
```

---

## 📊 数据导出格式

### CSV 格式
```csv
title,price,url
Product 1,99.99,https://...
Product 2,149.99,https://...
```

### JSON 格式
```json
[
  {
    "title": "Product 1",
    "price": 99.99,
    "url": "https://..."
  }
]
```

### Excel 格式
- 支持多 Sheet
- 自动格式化
- 数据验证

---

## 🔧 高级功能

### 自定义适配器

```python
from universal_scraper import BaseAdapter

class CustomAdapter(BaseAdapter):
    def parse(self, response):
        return {
            'title': response.css('h1::text').get(),
            'content': response.css('.content::text').get()
        }

scraper = UniversalScraper(adapter=CustomAdapter())
```

### 数据清洗

```python
from universal_scraper import DataCleaner

cleaner = DataCleaner()
cleaned_data = cleaner.clean(raw_data, rules={
    'price': 'float',
    'date': 'datetime',
    'title': 'strip'
})
```

### 增量爬取

```python
scraper = UniversalScraper(incremental=True, cache_file='cache.db')
new_items = scraper.scrape(url)  # 只返回新数据
```

---

## 📁 项目结构

```
universal-web-scraper/
├── SKILL.md              # OpenClaw Skill 描述
├── README.md             # 本文档
├── requirements.txt      # 依赖列表
├── scripts/
│   ├── scrape.py         # 爬取脚本
│   ├── batch_scrape.py   # 批量爬取
│   └── export.py         # 数据导出
├── config/
│   └── default.yaml      # 默认配置
├── adapters/
│   ├── ecommerce.py      # 电商适配器
│   ├── job.py            # 招聘适配器
│   ├── news.py           # 新闻适配器
│   └── generic.py        # 通用适配器
└── references/
    └── .env.example      # 环境变量模板
```

---

## 🛡️ 反爬虫策略

### 1. User-Agent 轮换
```python
scraper = UniversalScraper(rotate_user_agent=True)
```

### 2. 代理池
```python
scraper = UniversalScraper(proxy_pool=['proxy1', 'proxy2'])
```

### 3. 请求延迟
```python
scraper = UniversalScraper(delay=(1, 3))  # 随机延迟 1-3 秒
```

### 4. JavaScript 渲染
```python
scraper = UniversalScraper(render_js=True, headless=True)
```

---

## 🎓 展示价值

### 数据爬取能力 ⭐⭐⭐⭐⭐
- 多站点支持
- 智能反爬虫
- 高效并发

### 数据处理能力 ⭐⭐⭐⭐⭐
- 数据清洗
- 格式转换
- 质量验证

### 工程能力 ⭐⭐⭐⭐⭐
- 模块化设计
- 可扩展架构
- 完整文档

---

## 🔧 故障排除

### 常见问题

**Q: 爬取失败**
```
A: 检查网络连接和目标网站状态
   - 尝试使用代理
   - 增加重试次数
   - 启用 JavaScript 渲染
```

**Q: 数据不完整**
```
A: 检查选择器
   - 使用浏览器开发者工具验证
   - 尝试不同的适配器
   - 启用自适应模式
```

**Q: 被封禁**
```
A: 加强反爬虫措施
   - 启用代理轮换
   - 增加请求延迟
   - 使用更真实的 User-Agent
```

---

## 📄 许可证

MIT License

---

## ⚠️ 免责声明

本工具仅供学习和研究目的。使用时请遵守目标网站的 robots.txt 和服务条款。

---

_基于 [Scrapling](https://github.com/D4Vinci/Scrapling) 和 [Crawlee-Python](https://github.com/apify/crawlee-python) 开发_
_OpenClaw Skill 封装版本_
