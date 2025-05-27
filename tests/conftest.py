import pytest
import os
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_context():
    """创建浏览器上下文的 fixture"""
    with sync_playwright() as p:
        # 从环境变量获取配置
        headless = os.getenv("HEADLESS", "true").lower() == "true"
        browser_name = os.getenv("BROWSER", "chromium")
        
        # 启动浏览器
        if browser_name == "firefox":
            browser = p.firefox.launch(headless=headless)
        elif browser_name == "webkit":
            browser = p.webkit.launch(headless=headless)
        else:
            browser = p.chromium.launch(headless=headless)
        
        # 创建上下文
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        yield context
        
        # 清理
        context.close()
        browser.close()

@pytest.fixture
def page(browser_context):
    """创建页面的 fixture"""
    page = browser_context.new_page()
    
    # 设置默认超时时间
    page.set_default_timeout(30000)
    
    yield page
    
    # 清理
    page.close()

def pytest_configure(config):
    """pytest 配置"""
    # 添加自定义标记
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "smoke: marks tests as smoke tests")
    config.addinivalue_line("markers", "integration: marks tests as integration tests") 