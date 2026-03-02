#!/usr/bin/env python3
"""CLI interface for Universal Web Scraper"""
import asyncio
import argparse
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from scraper import UniversalScraper
from adapters import EcommerceAdapter, JobAdapter, NewsAdapter, GenericAdapter
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    parser = argparse.ArgumentParser(description='Universal Web Scraper')
    parser.add_argument('--url', help='Single URL to scrape')
    parser.add_argument('--urls', help='File with URLs (one per line)')
    parser.add_argument('--adapter', default='generic', choices=['generic', 'ecommerce', 'job', 'news'])
    parser.add_argument('--output', default='output/results.csv', help='Output file')
    parser.add_argument('--format', default='csv', choices=['csv', 'json', 'excel'])
    parser.add_argument('--config', help='Config file path')
    
    args = parser.parse_args()
    
    if not args.url and not args.urls:
        parser.error('Either --url or --urls must be provided')
    
    # Create scraper
    scraper = UniversalScraper(config_path=args.config)
    
    # Get URLs
    if args.url:
        urls = [args.url]
    else:
        with open(args.urls, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    
    logger.info(f"Scraping {len(urls)} URLs with {args.adapter} adapter")
    
    # Define selectors based on adapter
    selectors = {
        'generic': {'title': 'h1, h2', 'content': 'p'},
        'ecommerce': {'title': '.product-title, h2', 'price': '.price, [class*="price"]'},
        'job': {'title': '.job-title, h2', 'company': '.company'},
        'news': {'title': 'h1', 'content': 'article, .content'}
    }
    
    # Scrape
    df = await scraper.scrape_multiple(urls, selectors[args.adapter])
    
    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scraper.save_results(df, str(output_path), format=args.format)
    
    logger.info(f"✅ Scraped {len(df)} items, saved to {output_path}")


if __name__ == '__main__':
    asyncio.run(main())
