"""E-commerce adapter"""
from typing import Dict, List, Any
from bs4 import BeautifulSoup
from .base import BaseAdapter


class EcommerceAdapter(BaseAdapter):
    """Adapter for e-commerce websites"""
    
    def __init__(self):
        super().__init__()
        self.selectors = {
            'amazon': {
                'container': 'div[data-component-type="s-search-result"]',
                'title': 'h2 a span',
                'price': '.a-price-whole',
                'rating': '.a-icon-alt',
                'image': '.s-image',
                'link': 'h2 a'
            },
            'ebay': {
                'container': '.s-item',
                'title': '.s-item__title',
                'price': '.s-item__price',
                'rating': '.x-star-rating',
                'image': '.s-item__image-img',
                'link': '.s-item__link'
            },
            'generic': {
                'container': '.product, .item, [class*="product"]',
                'title': 'h2, h3, .title, [class*="title"]',
                'price': '.price, [class*="price"]',
                'rating': '.rating, [class*="rating"]',
                'image': 'img',
                'link': 'a'
            }
        }
    
    def parse(self, html: str, url: str) -> List[Dict[str, Any]]:
        """Parse e-commerce page"""
        soup = BeautifulSoup(html, 'lxml')
        results = []
        
        # Detect site type
        site_type = self._detect_site_type(url)
        selectors = self.selectors.get(site_type, self.selectors['generic'])
        
        # Find all product containers
        containers = soup.select(selectors['container'])
        
        for container in containers:
            try:
                item = {}
                
                # Extract title
                title_elem = container.select_one(selectors['title'])
                item['title'] = self.clean_text(title_elem.get_text()) if title_elem else ""
                
                # Extract price
                price_elem = container.select_one(selectors['price'])
                item['price'] = self.extract_price(price_elem.get_text()) if price_elem else 0.0
                
                # Extract rating
                rating_elem = container.select_one(selectors['rating'])
                item['rating'] = self.extract_rating(rating_elem.get_text()) if rating_elem else 0.0
                
                # Extract image
                image_elem = container.select_one(selectors['image'])
                item['image'] = image_elem.get('src', '') if image_elem else ""
                
                # Extract link
                link_elem = container.select_one(selectors['link'])
                item['url'] = link_elem.get('href', '') if link_elem else ""
                
                if item['title']:  # Only add if we got a title
                    results.append(item)
                    
            except Exception as e:
                continue
        
        return results
    
    def _detect_site_type(self, url: str) -> str:
        """Detect e-commerce site type from URL"""
        url_lower = url.lower()
        if 'amazon' in url_lower:
            return 'amazon'
        elif 'ebay' in url_lower:
            return 'ebay'
        return 'generic'
