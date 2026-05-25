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
    
    def remove_duplicates(self, data, subset: List[str] = None,
                           key: str = None):
        """Remove duplicates from DataFrame or list[dict].

        - ``data`` 是 DataFrame → 按 subset 列去重，返回 DataFrame
        - ``data`` 是 list[dict] → 按 ``key`` 字段去重（保留第一次出现），
          返回 list[dict]；key=None 时按完整 dict 去重
        """
        if isinstance(data, pd.DataFrame):
            return data.drop_duplicates(subset=subset)
        if not isinstance(data, list):
            raise TypeError(
                f"data 必须是 DataFrame 或 list[dict]，得到 {type(data).__name__}"
            )
        if key is None:
            seen: List = []
            out = []
            for item in data:
                if item not in seen:
                    seen.append(item)
                    out.append(item)
            return out
        seen_keys = set()
        out = []
        for item in data:
            k = item.get(key) if isinstance(item, dict) else None
            if k not in seen_keys:
                seen_keys.add(k)
                out.append(item)
        return out
    
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

    # --- v2 新增：处理原始 dict / 字符串而非 DataFrame ---------------------

    @staticmethod
    def clean_html(text: str) -> str:
        """剥 HTML 标签，保留可见文本。

        简单 regex 实现（不依赖 BeautifulSoup）。多个连续标签之间的文本
        会用空格分隔，避免 ``<b>A</b><b>B</b>`` 被拼成 "AB"。
        """
        if not text:
            return ""
        # 把所有 tag 替换成空格，再 normalize 空白
        no_tags = re.sub(r"<[^>]+>", " ", str(text))
        # decode 常见 HTML entity
        no_tags = (no_tags.replace("&nbsp;", " ")
                          .replace("&amp;", "&")
                          .replace("&lt;", "<")
                          .replace("&gt;", ">")
                          .replace("&quot;", '"')
                          .replace("&#39;", "'"))
        # 多空白合一
        return " ".join(no_tags.split()).strip()

    @staticmethod
    def normalize(text: str) -> str:
        """规范化文本：去首尾空白 + 多空白合一 + 换行 / tab 转空格。"""
        if not text:
            return ""
        return " ".join(str(text).split()).strip()

    @staticmethod
    def remove_empty(data: List[Dict[str, Any]],
                      fields: List[str]) -> List[Dict[str, Any]]:
        """从 list[dict] 删除必填字段为空（None / "" / 全空白）的项。"""
        if not data:
            return []
        out: List[Dict[str, Any]] = []
        for item in data:
            ok = True
            for f in fields:
                v = item.get(f)
                if v is None:
                    ok = False
                    break
                if isinstance(v, str) and not v.strip():
                    ok = False
                    break
            if ok:
                out.append(item)
        return out


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
