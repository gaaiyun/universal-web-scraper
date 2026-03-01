#!/usr/bin/env python3
"""
E-commerce scraper - Example implementation
"""

import asyncio
from scraper import UniversalScraper
import pandas as pd


class EcommerceScraper(UniversalScraper):
    """Specialized scraper for e-commerce sites"""
    
    def __init__(self):
        super().__init__()
        self.selectors = {
            'amazon': {
                'title': 'h2.s-line-clamp-2',
                'price': '.a-price-whole',
                'rating': '.a-icon-alt'
            },
            'ebay': {
                'title': '.s-item__title',
                'price': '.s-item__price',
                'rating': '.x-star-rating'
            }
        }
    
    async def scrape_amazon(self, search_query: str, pages: int = 3) -> pd.DataFrame:
        """Scrape Amazon search results"""
        urls = [
            f"https://www.amazon.com/s?k={search_query}&page={i}"
            for i in range(1, pages + 1)
        ]
        return await self.scrape_multiple(urls, self.selectors['amazon'])
    
    async def scrape_ebay(self, search_query: str, pages: int = 3) -> pd.DataFrame:
        """Scrape eBay search results"""
        urls = [
            f"https://www.ebay.com/sch/i.html?_nkw={search_query}&_pgn={i}"
            for i in range(1, pages + 1)
        ]
        return await self.scrape_multiple(urls, self.selectors['ebay'])


async def main():
    scraper = EcommerceScraper()
    
    # Scrape Amazon
    df_amazon = await scraper.scrape_amazon('laptop', pages=2)
    scraper.save_results(df_amazon, 'output/amazon_laptops.csv')
    
    # Scrape eBay
    df_ebay = await scraper.scrape_ebay('laptop', pages=2)
    scraper.save_results(df_ebay, 'output/ebay_laptops.csv')


if __name__ == '__main__':
    asyncio.run(main())
