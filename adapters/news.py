"""News article adapter"""
from typing import Dict, List, Any
from bs4 import BeautifulSoup
from datetime import datetime
from .base import BaseAdapter


class NewsAdapter(BaseAdapter):
    """Adapter for news websites"""
    
    def __init__(self):
        super().__init__()
        self.selectors = {
            'generic': {
                'container': 'article, .article, [class*="article"]',
                'title': 'h1, h2, .title, [class*="title"]',
                'author': '.author, [class*="author"]',
                'date': 'time, .date, [class*="date"]',
                'content': '.content, .article-body, [class*="content"]',
                'tags': '.tag, .category, [class*="tag"]',
                'link': 'a'
            }
        }
    
    def parse(self, html: str, url: str) -> List[Dict[str, Any]]:
        """Parse news page"""
        soup = BeautifulSoup(html, 'lxml')
        results = []
        
        selectors = self.selectors['generic']
        
        # Find all article containers
        containers = soup.select(selectors['container'])
        
        for container in containers:
            try:
                item = {}
                
                # Extract title
                title_elem = container.select_one(selectors['title'])
                item['title'] = self.clean_text(title_elem.get_text()) if title_elem else ""
                
                # Extract author
                author_elem = container.select_one(selectors['author'])
                item['author'] = self.clean_text(author_elem.get_text()) if author_elem else ""
                
                # Extract date
                date_elem = container.select_one(selectors['date'])
                item['date'] = self._extract_date(date_elem) if date_elem else ""
                
                # Extract content
                content_elem = container.select_one(selectors['content'])
                item['content'] = self.clean_text(content_elem.get_text()) if content_elem else ""
                
                # Extract tags
                tag_elems = container.select(selectors['tags'])
                item['tags'] = [self.clean_text(tag.get_text()) for tag in tag_elems]
                
                # Extract link
                link_elem = container.select_one(selectors['link'])
                item['url'] = link_elem.get('href', '') if link_elem else ""
                
                if item['title']:  # Only add if we got a title
                    results.append(item)
                    
            except Exception as e:
                continue
        
        return results
    
    def _extract_date(self, elem) -> str:
        """Extract and normalize date"""
        if elem.has_attr('datetime'):
            return elem['datetime']
        text = self.clean_text(elem.get_text())
        return text
