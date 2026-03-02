"""Generic adapter for any website"""
from typing import Dict, List, Any
from bs4 import BeautifulSoup
from .base import BaseAdapter


class GenericAdapter(BaseAdapter):
    """Generic adapter that works with custom selectors"""
    
    def __init__(self, selectors: Dict[str, str] = None):
        super().__init__()
        self.custom_selectors = selectors or {}
    
    def parse(self, html: str, url: str) -> List[Dict[str, Any]]:
        """Parse page with custom selectors"""
        soup = BeautifulSoup(html, 'lxml')
        results = []
        
        if not self.custom_selectors:
            # Auto-detect common patterns
            return self._auto_parse(soup)
        
        # Use custom selectors
        item = {}
        for field, selector in self.custom_selectors.items():
            elements = soup.select(selector)
            if elements:
                if len(elements) == 1:
                    item[field] = self.clean_text(elements[0].get_text())
                else:
                    item[field] = [self.clean_text(elem.get_text()) for elem in elements]
        
        if item:
            results.append(item)
        
        return results
    
    def _auto_parse(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Auto-detect and parse common patterns"""
        results = []
        
        # Try to find main content
        main_content = soup.select_one('main, article, .content, #content')
        if not main_content:
            main_content = soup
        
        # Extract common elements
        item = {}
        
        # Title
        title = main_content.select_one('h1, h2, .title')
        if title:
            item['title'] = self.clean_text(title.get_text())
        
        # Description/Content
        content = main_content.select_one('p, .description, .content')
        if content:
            item['content'] = self.clean_text(content.get_text())
        
        # Links
        links = main_content.select('a[href]')
        if links:
            item['links'] = [link.get('href') for link in links[:10]]
        
        # Images
        images = main_content.select('img[src]')
        if images:
            item['images'] = [img.get('src') for img in images[:10]]
        
        if item:
            results.append(item)
        
        return results
