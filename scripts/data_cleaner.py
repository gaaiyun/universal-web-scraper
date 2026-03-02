#!/usr/bin/env python3
"""Data cleaning utilities"""
import pandas as pd
import re
from typing import Dict, Any, List
from datetime import datetime


class DataCleaner:
    """Clean and normalize scraped data"""
    
    def __init__(self):
        self.cleaning_rules = {
            'price': self._clean_price,
            'rating': self._clean_rating,
            'date': self._clean_date,
            'text': self._clean_text,
            'url': self._clean_url
        }
    
    def clean(self, df: pd.DataFrame, rules: Dict[str, str] = None) -> pd.DataFrame:
        """Clean dataframe based on rules"""
        df_clean = df.copy()
        
        if rules:
            for column, rule_type in rules.items():
                if column in df_clean.columns:
                    cleaner = self.cleaning_rules.get(rule_type)
                    if cleaner:
                        df_clean[column] = df_clean[column].apply(cleaner)
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Remove rows with all NaN
        df_clean = df_clean.dropna(how='all')
        
        return df_clean
    
    def _clean_price(self, value: Any) -> float:
        """Clean price values"""
        if pd.isna(value):
            return 0.0
        
        text = str(value)
        # Remove currency symbols and commas
        text = re.sub(r'[^\d.]', '', text)
        
        try:
            return float(text)
        except:
            return 0.0
    
    def _clean_rating(self, value: Any) -> float:
        """Clean rating values"""
        if pd.isna(value):
            return 0.0
        
        text = str(value)
        # Extract first number
        match = re.search(r'(\d+\.?\d*)', text)
        
        try:
            return float(match.group(1)) if match else 0.0
        except:
            return 0.0
    
    def _clean_date(self, value: Any) -> str:
        """Clean date values"""
        if pd.isna(value):
            return ""
        
        text = str(value).strip()
        
        # Try to parse common date formats
        date_formats = [
            '%Y-%m-%d',
            '%d/%m/%Y',
            '%m/%d/%Y',
            '%Y-%m-%d %H:%M:%S',
            '%d %B %Y',
            '%B %d, %Y'
        ]
        
        for fmt in date_formats:
            try:
                dt = datetime.strptime(text, fmt)
                return dt.strftime('%Y-%m-%d')
            except:
                continue
        
        return text
    
    def _clean_text(self, value: Any) -> str:
        """Clean text values"""
        if pd.isna(value):
            return ""
        
        text = str(value)
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Remove special characters
        text = re.sub(r'[^\w\s\-.,!?]', '', text)
        
        return text.strip()
    
    def _clean_url(self, value: Any) -> str:
        """Clean URL values"""
        if pd.isna(value):
            return ""
        
        url = str(value).strip()
        
        # Add protocol if missing
        if url and not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        return url
    
    def remove_duplicates(self, df: pd.DataFrame, subset: List[str] = None) -> pd.DataFrame:
        """Remove duplicate rows"""
        return df.drop_duplicates(subset=subset)
    
    def fill_missing(self, df: pd.DataFrame, strategy: str = 'drop') -> pd.DataFrame:
        """Handle missing values"""
        if strategy == 'drop':
            return df.dropna()
        elif strategy == 'fill':
            return df.fillna('')
        elif strategy == 'forward':
            return df.fillna(method='ffill')
        return df
    
    def validate_data(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """Validate dataframe has required columns"""
        missing = set(required_columns) - set(df.columns)
        if missing:
            print(f"Missing columns: {missing}")
            return False
        return True


if __name__ == '__main__':
    # Example usage
    cleaner = DataCleaner()
    
    # Sample data
    df = pd.DataFrame({
        'title': ['Product 1', '  Product 2  ', 'Product 3'],
        'price': ['$99.99', '149,99', '199'],
        'rating': ['4.5 stars', '5/5', '3.8']
    })
    
    print("Original data:")
    print(df)
    
    # Clean data
    df_clean = cleaner.clean(df, rules={
        'price': 'price',
        'rating': 'rating',
        'title': 'text'
    })
    
    print("\nCleaned data:")
    print(df_clean)
