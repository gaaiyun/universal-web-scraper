"""Base adapter class"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any
from bs4 import BeautifulSoup


class BaseAdapter(ABC):
    """Base class for all adapters"""
    
    def __init__(self):
        self.selectors = {}
    
    @abstractmethod
    def parse(self, html: str, url: str) -> List[Dict[str, Any]]:
        """Parse HTML and extract data"""
        pass
    
    def clean_text(self, text: str) -> str:
        """Clean extracted text"""
        if not text:
            return ""
        return " ".join(text.split()).strip()
    
    def extract_price(self, text: str) -> float:
        """Extract price from text"""
        import re
        if not text:
            return 0.0
        match = re.search(r'[\d,]+\.?\d*', text.replace(',', ''))
        return float(match.group()) if match else 0.0
    
    def extract_rating(self, text: str) -> float:
        """Extract rating from text"""
        import re
        if not text:
            return 0.0
        match = re.search(r'(\d+\.?\d*)\s*out of\s*(\d+)|(\d+\.?\d*)\s*stars?|(\d+\.?\d*)/(\d+)', text)
        if match:
            groups = [g for g in match.groups() if g]
            return float(groups[0]) if groups else 0.0
        return 0.0
