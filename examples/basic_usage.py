#!/usr/bin/env python3
"""
Basic usage examples for Universal Web Scraper
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from scraper import UniversalScraper


async def example_1_single_page():
    """Example 1: Scrape a single page"""
    print("Example 1: Single page scraping")
    
    scraper = UniversalScraper()
    
    url = "https://example.com/products"
    selectors = {
        'title': '.product-title',
        'price': '.product-price'
    }
    
    data = await scraper.scrape_url(url, selectors)
    print(f"Scraped data: {data}")


async def example_2_multiple_pages():
    """Example 2: Scrape multiple pages"""
    print("\nExample 2: Multiple pages scraping")
    
    scraper = UniversalScraper()
    
    urls = [
        "https://example.com/products/page1",
        "https://example.com/products/page2",
        "https://example.com/products/page3"
    ]
    
    selectors = {
        'title': '.product-title',
        'price': '.product-price',
        'rating': '.product-rating'
    }
    
    df = await scraper.scrape_multiple(urls, selectors)
    print(f"Scraped {len(df)} items")
    print(df.head())
    
    # Save results
    scraper.save_results(df, 'output/products.csv')


async def example_3_with_config():
    """Example 3: Use configuration file"""
    print("\nExample 3: Scraping with config")
    
    scraper = UniversalScraper(config_path='config/default.yaml')
    
    urls = ["https://example.com/products"]
    selectors = {'title': '.product-title'}
    
    df = await scraper.scrape_multiple(urls, selectors)
    scraper.save_results(df, 'output/products_with_config.csv')


async def main():
    """Run all examples"""
    await example_1_single_page()
    await example_2_multiple_pages()
    await example_3_with_config()


if __name__ == '__main__':
    asyncio.run(main())
