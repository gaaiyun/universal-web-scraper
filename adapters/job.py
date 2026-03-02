"""Job listing adapter"""
from typing import Dict, List, Any
from bs4 import BeautifulSoup
from .base import BaseAdapter


class JobAdapter(BaseAdapter):
    """Adapter for job listing websites"""
    
    def __init__(self):
        super().__init__()
        self.selectors = {
            'indeed': {
                'container': '.job_seen_beacon',
                'title': '.jobTitle',
                'company': '.companyName',
                'location': '.companyLocation',
                'salary': '.salary-snippet',
                'description': '.job-snippet',
                'link': 'a.jcs-JobTitle'
            },
            'linkedin': {
                'container': '.job-card-container',
                'title': '.job-card-list__title',
                'company': '.job-card-container__company-name',
                'location': '.job-card-container__metadata-item',
                'salary': '.job-card-salary',
                'description': '.job-card-list__snippet',
                'link': 'a.job-card-list__title'
            },
            'generic': {
                'container': '.job, .position, [class*="job"]',
                'title': 'h2, h3, .title, [class*="title"]',
                'company': '.company, [class*="company"]',
                'location': '.location, [class*="location"]',
                'salary': '.salary, [class*="salary"]',
                'description': '.description, [class*="description"]',
                'link': 'a'
            }
        }
    
    def parse(self, html: str, url: str) -> List[Dict[str, Any]]:
        """Parse job listing page"""
        soup = BeautifulSoup(html, 'lxml')
        results = []
        
        # Detect site type
        site_type = self._detect_site_type(url)
        selectors = self.selectors.get(site_type, self.selectors['generic'])
        
        # Find all job containers
        containers = soup.select(selectors['container'])
        
        for container in containers:
            try:
                item = {}
                
                # Extract title
                title_elem = container.select_one(selectors['title'])
                item['title'] = self.clean_text(title_elem.get_text()) if title_elem else ""
                
                # Extract company
                company_elem = container.select_one(selectors['company'])
                item['company'] = self.clean_text(company_elem.get_text()) if company_elem else ""
                
                # Extract location
                location_elem = container.select_one(selectors['location'])
                item['location'] = self.clean_text(location_elem.get_text()) if location_elem else ""
                
                # Extract salary
                salary_elem = container.select_one(selectors['salary'])
                item['salary'] = self.clean_text(salary_elem.get_text()) if salary_elem else ""
                
                # Extract description
                desc_elem = container.select_one(selectors['description'])
                item['description'] = self.clean_text(desc_elem.get_text()) if desc_elem else ""
                
                # Extract link
                link_elem = container.select_one(selectors['link'])
                item['url'] = link_elem.get('href', '') if link_elem else ""
                
                if item['title']:  # Only add if we got a title
                    results.append(item)
                    
            except Exception as e:
                continue
        
        return results
    
    def _detect_site_type(self, url: str) -> str:
        """Detect job site type from URL"""
        url_lower = url.lower()
        if 'indeed' in url_lower:
            return 'indeed'
        elif 'linkedin' in url_lower:
            return 'linkedin'
        return 'generic'
