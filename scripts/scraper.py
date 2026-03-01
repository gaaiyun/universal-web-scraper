#!/usr/bin/env python3
"""
Universal Web Scraper - Main scraper implementation
"""

import asyncio
from typing import Dict, List, Optional
from scrapling import Fetcher
from bs4 import BeautifulSoup
import pandas as pd
import yaml
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalScraper:
    """Universal web scraper with anti-detection"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.fetcher = Fetcher(
            auto_match=True,
            stealth=True
        )
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    async def scrape_url(self, url: str, selectors: Dict[str, str]) -> Dict:
        """Scrape single URL"""
        try:
            logger.info(f"Scraping: {url}")
            response = await self.fetcher.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            
            data = {}
            for field, selector in selectors.items():
                elements = soup.select(selector)
                data[field] = [elem.get_text(strip=True) for elem in elements]
            
            return data
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
            return {}
    
    async def scrape_multiple(self, urls: List[str], selectors: Dict[str, str]) -> pd.DataFrame:
        """Scrape multiple URLs"""
        tasks = [self.scrape_url(url, selectors) for url in urls]
        results = await asyncio.gather(*tasks)
        return pd.DataFrame(results)
    
    def save_results(self, df: pd.DataFrame, output_path: str, format: str = 'csv'):
        """Save scraping results"""
        if format == 'csv':
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
        elif format == 'json':
            df.to_json(output_path, orient='records', force_ascii=False, indent=2)
        elif format == 'excel':
            df.to_excel(output_path, index=False)
        logger.info(f"Results saved to {output_path}")


async def main():
    """Example usage"""
    scraper = UniversalScraper()
    
    # Example: Scrape product listings
    urls = [
        "https://example.com/products/page1",
        "https://example.com/products/page2"
    ]
    
    selectors = {
        'title': '.product-title',
        'price': '.product-price',
        'rating': '.product-rating'
    }
    
    df = await scraper.scrape_multiple(urls, selectors)
    scraper.save_results(df, 'output/products.csv')


if __name__ == '__main__':
    asyncio.run(main())
