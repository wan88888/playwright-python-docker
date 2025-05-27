import pytest
from playwright.sync_api import sync_playwright

def test_baidu_search():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.baidu.com")
        assert "百度" in page.title()
        browser.close()