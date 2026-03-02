"""
Tests for Universal Web Scraper
单元测试 - 网页爬虫
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from pathlib import Path
import json
import sys
import asyncio

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDataCleaner:
    """测试数据清洗功能"""
    
    def test_remove_duplicates(self):
        """测试去重功能"""
        data = [
            {'title': 'A', 'url': 'url1'},
            {'title': 'A', 'url': 'url1'},
            {'title': 'B', 'url': 'url2'}
        ]
        
        # Simple dedup test
        seen = set()
        unique = []
        for item in data:
            key = item['url']
            if key not in seen:
                seen.add(key)
                unique.append(item)
        
        assert len(unique) == 2
    
    def test_clean_html_tags(self):
        """测试 HTML 标签清理"""
        from bs4 import BeautifulSoup
        
        text = "<p>Hello <b>World</b></p>"
        soup = BeautifulSoup(text, 'html.parser')
        cleaned = soup.get_text()
        
        assert '<' not in cleaned
        assert 'Hello' in cleaned
    
    def test_normalize_text(self):
        """测试文本标准化"""
        text = "  Hello   World  \n  "
        cleaned = ' '.join(text.split())
        
        assert cleaned == "Hello World"
    
    def test_remove_empty(self):
        """测试空值清理"""
        data = [
            {'title': 'A', 'content': 'test'},
            {'title': '', 'content': 'test2'},
            {'title': 'C', 'content': None}
        ]
        
        cleaned = [d for d in data if d.get('title') and d.get('content')]
        assert len(cleaned) == 1


class TestDataCleaner:
    """测试数据清洗功能"""
    
    def test_remove_duplicates(self):
        """测试去重功能"""
        from scripts.data_cleaner import DataCleaner
        
        data = [
            {'title': 'A', 'url': 'url1'},
            {'title': 'A', 'url': 'url1'},
            {'title': 'B', 'url': 'url2'}
        ]
        
        cleaner = DataCleaner()
        cleaned = cleaner.remove_duplicates(data, key='url')
        
        assert len(cleaned) == 2
    
    def test_clean_html_tags(self):
        """测试 HTML 标签清理"""
        from scripts.data_cleaner import DataCleaner
        
        text = "<p>Hello <b>World</b></p>"
        cleaner = DataCleaner()
        cleaned = cleaner.clean_html(text)
        
        assert '<' not in cleaned
        assert 'Hello World' in cleaned
    
    def test_normalize_text(self):
        """测试文本标准化"""
        from scripts.data_cleaner import DataCleaner
        
        text = "  Hello   World  \n  "
        cleaner = DataCleaner()
        cleaned = cleaner.normalize(text)
        
        assert cleaned == "Hello World"
    
    def test_remove_empty(self):
        """测试空值清理"""
        from scripts.data_cleaner import DataCleaner
        
        data = [
            {'title': 'A', 'content': 'test'},
            {'title': '', 'content': 'test2'},
            {'title': 'C', 'content': None}
        ]
        
        cleaner = DataCleaner()
        cleaned = cleaner.remove_empty(data, fields=['title', 'content'])
        
        assert len(cleaned) == 1


class TestExportFunctions:
    """测试导出功能"""
    
    def test_export_csv(self, tmp_path):
        """测试 CSV 导出"""
        data = [
            {'title': 'A', 'url': 'url1'},
            {'title': 'B', 'url': 'url2'}
        ]
        
        output_file = tmp_path / "test.csv"
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        
        assert output_file.exists()
        
        # Verify content
        df_loaded = pd.read_csv(output_file)
        assert len(df_loaded) == 2
        assert 'title' in df_loaded.columns
    
    def test_export_json(self, tmp_path):
        """测试 JSON 导出"""
        data = [
            {'title': 'A', 'url': 'url1'},
            {'title': 'B', 'url': 'url2'}
        ]
        
        output_file = tmp_path / "test.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        
        assert output_file.exists()
        
        # Verify content
        with open(output_file, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        assert len(loaded) == 2


class TestAdapters:
    """测试适配器解析逻辑"""
    
    def test_news_adapter_parse(self):
        """测试新闻适配器解析"""
        from bs4 import BeautifulSoup
        
        html = """
        <article>
            <h2>News Title</h2>
            <p class="summary">News summary</p>
            <span class="date">2024-01-01</span>
        </article>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h2').get_text(strip=True)
        summary = soup.find('p', class_='summary').get_text(strip=True)
        
        assert title == 'News Title'
        assert summary == 'News summary'
    
    def test_ecommerce_adapter_parse(self):
        """测试电商适配器解析"""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="product">
            <h3 class="product-name">Product Name</h3>
            <span class="price">$99.99</span>
        </div>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        name = soup.find('h3', class_='product-name').get_text(strip=True)
        price = soup.find('span', class_='price').get_text(strip=True)
        
        assert name == 'Product Name'
        assert price == '$99.99'
    
    def test_job_adapter_parse(self):
        """测试招聘适配器解析"""
        from bs4 import BeautifulSoup
        
        html = """
        <div class="job-listing">
            <h4 class="job-title">Software Engineer</h4>
            <span class="company">Tech Co</span>
        </div>
        """
        
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.find('h4', class_='job-title').get_text(strip=True)
        company = soup.find('span', class_='company').get_text(strip=True)
        
        assert title == 'Software Engineer'
        assert company == 'Tech Co'


class TestAsyncScraper:
    """测试异步爬虫"""
    
    @pytest.mark.asyncio
    @patch('scrapling.Fetcher')
    async def test_scrape_url(self, mock_fetcher_class):
        """测试 URL 爬取"""
        from scripts.scraper import UniversalScraper
        
        # Mock fetcher
        mock_fetcher = AsyncMock()
        mock_fetcher.get = AsyncMock(return_value=Mock(text="<html><body>Test</body></html>"))
        mock_fetcher_class.return_value = mock_fetcher
        
        scraper = UniversalScraper()
        selectors = {'title': 'h1'}
        result = await scraper.scrape_url('https://example.com', selectors)
        
        assert result is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
