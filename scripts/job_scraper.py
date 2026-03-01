#!/usr/bin/env python3
"""
Job listing scraper - Example implementation
"""

import asyncio
from scraper import UniversalScraper
import pandas as pd


class JobScraper(UniversalScraper):
    """Specialized scraper for job sites"""
    
    def __init__(self):
        super().__init__()
        self.selectors = {
            'indeed': {
                'title': '.jobTitle',
                'company': '.companyName',
                'location': '.companyLocation',
                'salary': '.salary-snippet'
            },
            'linkedin': {
                'title': '.job-card-list__title',
                'company': '.job-card-container__company-name',
                'location': '.job-card-container__metadata-item'
            }
        }
    
    async def scrape_indeed(self, job_title: str, location: str, pages: int = 3) -> pd.DataFrame:
        """Scrape Indeed job listings"""
        urls = [
            f"https://www.indeed.com/jobs?q={job_title}&l={location}&start={i*10}"
            for i in range(pages)
        ]
        return await self.scrape_multiple(urls, self.selectors['indeed'])
    
    async def scrape_linkedin(self, job_title: str, location: str, pages: int = 3) -> pd.DataFrame:
        """Scrape LinkedIn job listings"""
        urls = [
            f"https://www.linkedin.com/jobs/search?keywords={job_title}&location={location}&start={i*25}"
            for i in range(pages)
        ]
        return await self.scrape_multiple(urls, self.selectors['linkedin'])


async def main():
    scraper = JobScraper()
    
    # Scrape Indeed
    df_indeed = await scraper.scrape_indeed('data analyst', 'New York', pages=2)
    scraper.save_results(df_indeed, 'output/indeed_jobs.csv')
    
    # Scrape LinkedIn
    df_linkedin = await scraper.scrape_linkedin('data analyst', 'New York', pages=2)
    scraper.save_results(df_linkedin, 'output/linkedin_jobs.csv')


if __name__ == '__main__':
    asyncio.run(main())
