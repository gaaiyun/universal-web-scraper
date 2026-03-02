#!/usr/bin/env python3
"""Batch scraper for multiple URLs"""
import asyncio
import argparse
from pathlib import Path
from typing import List
import pandas as pd
from scraper import UniversalScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchScraper:
    """Scrape multiple URLs in batch"""
    
    def __init__(self, adapter: str = 'generic', max_concurrent: int = 5):
        self.scraper = UniversalScraper()
        self.adapter = adapter
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def scrape_with_limit(self, url: str, selectors: dict) -> dict:
        """Scrape with concurrency limit"""
        async with self.semaphore:
            return await self.scraper.scrape_url(url, selectors)
    
    async def scrape_batch(self, urls: List[str], selectors: dict) -> pd.DataFrame:
        """Scrape multiple URLs"""
        logger.info(f"Starting batch scrape of {len(urls)} URLs")
        
        tasks = [self.scrape_with_limit(url, selectors) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out errors
        valid_results = [r for r in results if not isinstance(r, Exception)]
        logger.info(f"Successfully scraped {len(valid_results)}/{len(urls)} URLs")
        
        return pd.DataFrame(valid_results)
    
    def load_urls_from_file(self, file_path: str) -> List[str]:
        """Load URLs from text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
        return urls


async def main():
    parser = argparse.ArgumentParser(description='Batch web scraper')
    parser.add_argument('--urls', required=True, help='File containing URLs (one per line)')
    parser.add_argument('--output', default='output/batch_results.csv', help='Output file')
    parser.add_argument('--adapter', default='generic', choices=['generic', 'ecommerce', 'job', 'news'])
    parser.add_argument('--max-concurrent', type=int, default=5, help='Max concurrent requests')
    parser.add_argument('--format', default='csv', choices=['csv', 'json', 'excel'])
    
    args = parser.parse_args()
    
    # Create batch scraper
    scraper = BatchScraper(adapter=args.adapter, max_concurrent=args.max_concurrent)
    
    # Load URLs
    urls = scraper.load_urls_from_file(args.urls)
    logger.info(f"Loaded {len(urls)} URLs from {args.urls}")
    
    # Define selectors based on adapter
    selectors = {
        'generic': {'title': 'h1, h2', 'content': 'p'},
        'ecommerce': {'title': '.product-title', 'price': '.price'},
        'job': {'title': '.job-title', 'company': '.company'},
        'news': {'title': 'h1', 'content': 'article'}
    }
    
    # Scrape
    df = await scraper.scrape_batch(urls, selectors[args.adapter])
    
    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.format == 'csv':
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
    elif args.format == 'json':
        df.to_json(output_path, orient='records', force_ascii=False, indent=2)
    elif args.format == 'excel':
        df.to_excel(output_path, index=False)
    
    logger.info(f"Results saved to {output_path}")
    logger.info(f"Total items scraped: {len(df)}")


if __name__ == '__main__':
    asyncio.run(main())
