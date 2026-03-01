---
name: universal-web-scraper
description: Universal web scraping framework for OpenClaw. Multi-site support, intelligent anti-bot, data cleaning and export. Perfect for showcasing data collection skills.
---

# Universal Web Scraper Skill

## 1. 什么时候用我？

当用户说：
- "爬取这个网站"
- "采集数据"
- "抓取商品信息"
- "监控价格"
- "收集招聘数据"
- 任何需要网页数据采集的场景

## 2. 我能做什么？

### 智能爬虫引擎
- **自适应解析** - 网站结构变化自动适配
- **智能反爬虫** - 绕过 Cloudflare、验证码
- **代理轮换** - 自动代理池管理
- **并发爬取** - 高效多线程/异步

### 多站点支持
- **电商平台** - 商品信息、价格监控
- **招聘网站** - 职位数据、薪资分析
- **新闻媒体** - 文章采集、舆情监控
- **社交媒体** - 用户数据、评论分析

### 数据处理
- **数据清洗** - 去重、格式化、验证
- **数据转换** - 结构化处理
- **多格式导出** - CSV, JSON, Excel, Database
- **增量更新** - 只爬取新数据

## 3. 使用示例

### 基础爬取
```bash
# 爬取单个页面
python scripts/scrape.py --url "https://example.com" --output data.json

# 使用适配器
python scripts/scrape.py --adapter ecommerce --url "https://shop.com"
```

### Python API
```python
from universal_scraper import UniversalScraper

# 电商数据采集
scraper = UniversalScraper(adapter='ecommerce')
products = scraper.scrape('https://shop.example.com')

# 招聘数据采集
scraper = UniversalScraper(adapter='job')
jobs = scraper.scrape('https://jobs.example.com')

# 导出数据
scraper.export(products, 'products.csv', format='csv')
```

### OpenClaw 调用
```python
# 在 OpenClaw 中自动触发
用户："帮我爬取这个网站的商品信息"
→ 自动调用 universal-web-scraper
→ 选择合适的适配器
→ 爬取并清洗数据
→ 导出结果
```

## 4. 配置说明

### 环境变量
```bash
# 代理配置
PROXY_URL=http://proxy.example.com:8080
PROXY_USERNAME=user
PROXY_PASSWORD=pass

# 数据库配置（可选）
DATABASE_URL=postgresql://user:pass@localhost/scraper
```

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
```

## 5. 适配器

### 电商适配器
```python
scraper = UniversalScraper(adapter='ecommerce')
products = scraper.scrape(url)
# 返回: title, price, image, description, rating
```

### 招聘适配器
```python
scraper = UniversalScraper(adapter='job')
jobs = scraper.scrape(url)
# 返回: title, company, salary, location, requirements
```

### 新闻适配器
```python
scraper = UniversalScraper(adapter='news')
articles = scraper.scrape(url)
# 返回: title, author, date, content, tags
```

### 通用适配器
```python
scraper = UniversalScraper(adapter='generic')
data = scraper.scrape(url, selectors={'title': 'h1'})
```

## 6. 反爬虫策略

- **User-Agent 轮换** - 模拟不同浏览器
- **代理池** - 自动切换 IP
- **请求延迟** - 随机延迟避免检测
- **JavaScript 渲染** - 处理动态页面

## 7. 展示价值

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

## 8. 依赖项

### Python 包
- Python 3.10+
- scrapling
- crawlee
- beautifulsoup4
- pandas
- playwright

### 安装
```bash
pip install scrapling crawlee beautifulsoup4 pandas playwright
playwright install
```

## 9. 注意事项

1. **遵守 robots.txt** - 尊重网站爬取规则
2. **合理延迟** - 避免对服务器造成压力
3. **数据使用** - 遵守数据使用条款
4. **法律合规** - 确保爬取行为合法

## 10. 故障排除

### 常见问题
- **爬取失败**: 检查网络和代理配置
- **数据不完整**: 验证选择器和适配器
- **被封禁**: 加强反爬虫措施

### 日志位置
- `~/.openclaw/workspace/logs/scraper.log`

---

_基于 Scrapling 和 Crawlee-Python 开发_
_OpenClaw Skill 封装版本_
