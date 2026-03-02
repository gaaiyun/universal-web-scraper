#!/usr/bin/env python3
"""Tests for adapters"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from adapters import EcommerceAdapter, JobAdapter, NewsAdapter, GenericAdapter


def test_ecommerce_adapter():
    """Test e-commerce adapter"""
    print("Testing E-commerce Adapter...")
    
    adapter = EcommerceAdapter()
    
    # Sample HTML
    html = """
    <div data-component-type="s-search-result">
        <h2><a><span>Test Product</span></a></h2>
        <span class="a-price-whole">99.99</span>
        <span class="a-icon-alt">4.5 out of 5 stars</span>
    </div>
    """
    
    results = adapter.parse(html, "https://amazon.com/test")
    
    assert len(results) > 0, "Should extract at least one product"
    assert 'title' in results[0], "Should have title"
    assert 'price' in results[0], "Should have price"
    
    print("✅ E-commerce adapter test passed")


def test_job_adapter():
    """Test job adapter"""
    print("Testing Job Adapter...")
    
    adapter = JobAdapter()
    
    # Sample HTML
    html = """
    <div class="job_seen_beacon">
        <span class="jobTitle">Software Engineer</span>
        <span class="companyName">Tech Corp</span>
        <div class="companyLocation">San Francisco, CA</div>
        <span class="salary-snippet">$120k-$150k</span>
    </div>
    """
    
    results = adapter.parse(html, "https://indeed.com/jobs")
    
    assert len(results) > 0, "Should extract at least one job"
    assert 'title' in results[0], "Should have title"
    assert 'company' in results[0], "Should have company"
    
    print("✅ Job adapter test passed")


def test_news_adapter():
    """Test news adapter"""
    print("Testing News Adapter...")
    
    adapter = NewsAdapter()
    
    # Sample HTML
    html = """
    <article>
        <h1>Breaking News</h1>
        <span class="author">John Doe</span>
        <time datetime="2024-01-01">January 1, 2024</time>
        <div class="content">This is the article content.</div>
    </article>
    """
    
    results = adapter.parse(html, "https://news.example.com")
    
    assert len(results) > 0, "Should extract at least one article"
    assert 'title' in results[0], "Should have title"
    assert 'author' in results[0], "Should have author"
    
    print("✅ News adapter test passed")


def test_generic_adapter():
    """Test generic adapter"""
    print("Testing Generic Adapter...")
    
    adapter = GenericAdapter({'title': 'h1', 'content': 'p'})
    
    # Sample HTML
    html = """
    <html>
        <h1>Page Title</h1>
        <p>Page content goes here.</p>
    </html>
    """
    
    results = adapter.parse(html, "https://example.com")
    
    assert len(results) > 0, "Should extract data"
    assert 'title' in results[0], "Should have title"
    
    print("✅ Generic adapter test passed")


if __name__ == '__main__':
    test_ecommerce_adapter()
    test_job_adapter()
    test_news_adapter()
    test_generic_adapter()
    
    print("\n🎉 All tests passed!")
