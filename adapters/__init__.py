"""Adapters for different website types"""
from .base import BaseAdapter
from .ecommerce import EcommerceAdapter
from .job import JobAdapter
from .news import NewsAdapter
from .generic import GenericAdapter

__all__ = ['BaseAdapter', 'EcommerceAdapter', 'JobAdapter', 'NewsAdapter', 'GenericAdapter']
