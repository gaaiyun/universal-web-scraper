"""
Advanced Web Scraping Templates
高级爬虫模板集合
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import json
import time
import random


class AdvancedScraperTemplates:
    """
    高级爬虫模板
    提供多种网站类型的爬取模板
    """
    
    def __init__(self):
        """初始化爬虫"""
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_news_site(self, url: str, max_articles: int = 50) -> List[Dict]:
        """
        新闻网站爬取模板
        
        Args:
            url: 新闻网站 URL
            max_articles: 最大文章数
            
        Returns:
            文章列表
        """
        articles = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找文章元素（需要根据实际网站调整选择器）
            article_elements = soup.find_all('article', limit=max_articles)
            
            for elem in article_elements:
                article = {
                    'title': self._safe_get_text(elem, 'h2'),
                    'summary': self._safe_get_text(elem, 'p'),
                    'url': self._safe_get_link(elem, 'a'),
                    'timestamp': datetime.now().isoformat(),
                    'source': url
                }
                articles.append(article)
                
        except Exception as e:
            print(f"Error scraping news: {e}")
        
        return articles
    
    def scrape_ecommerce_site(self, url: str, max_products: int = 100) -> List[Dict]:
        """
        电商网站爬取模板
        
        Args:
            url: 电商网站 URL
            max_products: 最大商品数
            
        Returns:
            商品列表
        """
        products = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找商品元素
            product_elements = soup.find_all(class_='product-item', limit=max_products)
            
            for elem in product_elements:
                product = {
                    'name': self._safe_get_text(elem, '.product-name'),
                    'price': self._safe_get_text(elem, '.product-price'),
                    'rating': self._safe_get_text(elem, '.product-rating'),
                    'url': self._safe_get_link(elem, 'a'),
                    'image': self._safe_get_src(elem, 'img'),
                    'timestamp': datetime.now().isoformat()
                }
                products.append(product)
                
        except Exception as e:
            print(f"Error scraping ecommerce: {e}")
        
        return products
    
    def scrape_job_board(self, url: str, max_jobs: int = 50) -> List[Dict]:
        """
        招聘网站爬取模板
        
        Args:
            url: 招聘网站 URL
            max_jobs: 最大职位数
            
        Returns:
            职位列表
        """
        jobs = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找职位元素
            job_elements = soup.find_all(class_='job-listing', limit=max_jobs)
            
            for elem in job_elements:
                job = {
                    'title': self._safe_get_text(elem, '.job-title'),
                    'company': self._safe_get_text(elem, '.company-name'),
                    'location': self._safe_get_text(elem, '.job-location'),
                    'salary': self._safe_get_text(elem, '.salary-range'),
                    'type': self._safe_get_text(elem, '.job-type'),
                    'url': self._safe_get_link(elem, 'a'),
                    'posted': self._safe_get_text(elem, '.posted-date'),
                    'timestamp': datetime.now().isoformat()
                }
                jobs.append(job)
                
        except Exception as e:
            print(f"Error scraping jobs: {e}")
        
        return jobs
    
    def scrape_blog(self, url: str, max_posts: int = 30) -> List[Dict]:
        """
        博客网站爬取模板
        
        Args:
            url: 博客网站 URL
            max_posts: 最大文章数
            
        Returns:
            文章列表
        """
        posts = []
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找文章元素
            post_elements = soup.find_all('article', limit=max_posts)
            
            for elem in post_elements:
                post = {
                    'title': self._safe_get_text(elem, 'h1'),
                    'author': self._safe_get_text(elem, '.author'),
                    'date': self._safe_get_text(elem, '.date'),
                    'tags': self._safe_get_all_text(elem, '.tag'),
                    'content': self._safe_get_text(elem, '.content'),
                    'url': self._safe_get_link(elem, 'a'),
                    'timestamp': datetime.now().isoformat()
                }
                posts.append(post)
                
        except Exception as e:
            print(f"Error scraping blog: {e}")
        
        return posts
    
    def _safe_get_text(self, elem, selector) -> Optional[str]:
        """安全获取文本"""
        try:
            child = elem.select_one(selector)
            return child.get_text(strip=True) if child else None
        except:
            return None
    
    def _safe_get_link(self, elem, selector) -> Optional[str]:
        """安全获取链接"""
        try:
            child = elem.select_one(selector)
            if child and child.has_attr('href'):
                return child['href']
            return None
        except:
            return None
    
    def _safe_get_src(self, elem, selector) -> Optional[str]:
        """安全获取图片源"""
        try:
            child = elem.select_one(selector)
            if child and child.has_attr('src'):
                return child['src']
            return None
        except:
            return None
    
    def _safe_get_all_text(self, elem, selector) -> List[str]:
        """安全获取所有匹配文本"""
        try:
            children = elem.select(selector)
            return [child.get_text(strip=True) for child in children]
        except:
            return []
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """保存到 CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Saved {len(data)} records to {filename}")
    
    def save_to_json(self, data: List[Dict], filename: str):
        """保存到 JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(data)} records to {filename}")


def demo_templates():
    """演示模板使用"""
    print("=" * 60)
    print("Advanced Web Scraping Templates Demo")
    print("=" * 60)
    
    scraper = AdvancedScraperTemplates()
    
    # 模拟数据
    print("\n1. News Site Template")
    print("-" * 60)
    sample_news = [
        {'title': 'News Article 1', 'summary': 'Summary...', 'source': 'example.com'},
        {'title': 'News Article 2', 'summary': 'Summary...', 'source': 'example.com'}
    ]
    print(f"Sample: {len(sample_news)} articles")
    
    print("\n2. Ecommerce Template")
    print("-" * 60)
    sample_products = [
        {'name': 'Product A', 'price': '$99.99', 'rating': '4.5'},
        {'name': 'Product B', 'price': '$149.99', 'rating': '4.8'}
    ]
    print(f"Sample: {len(sample_products)} products")
    
    print("\n3. Job Board Template")
    print("-" * 60)
    sample_jobs = [
        {'title': 'Software Engineer', 'company': 'Tech Co', 'location': 'Remote'},
        {'title': 'Data Analyst', 'company': 'Data Inc', 'location': 'NYC'}
    ]
    print(f"Sample: {len(sample_jobs)} jobs")
    
    print("\n4. Blog Template")
    print("-" * 60)
    sample_posts = [
        {'title': 'Blog Post 1', 'author': 'Author A', 'tags': ['tech', 'ai']},
        {'title': 'Blog Post 2', 'author': 'Author B', 'tags': ['data', 'ml']}
    ]
    print(f"Sample: {len(sample_posts)} posts")
    
    print("\n" + "=" * 60)
    print("Templates ready for customization!")
    print("=" * 60)


if __name__ == "__main__":
    demo_templates()
