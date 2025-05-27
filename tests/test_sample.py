import pytest
from playwright.sync_api import sync_playwright

@pytest.mark.smoke
def test_example_com(page):
    """测试 example.com 网站（稳定的测试目标）"""
    try:
        # 访问 example.com（更稳定的测试网站）
        page.goto("https://example.com", wait_until="networkidle")
        
        # 验证页面标题
        title = page.title()
        assert "Example Domain" in title, f"Expected 'Example Domain' in title, but got: {title}"
        
        # 验证页面内容
        heading = page.locator("h1")
        assert heading.is_visible(), "H1 heading should be visible"
        assert "Example Domain" in heading.text_content(), "H1 should contain 'Example Domain'"
        
    except Exception as e:
        # 失败时截图（用于调试）
        page.screenshot(path="test_failure_example.png")
        raise e

@pytest.mark.integration
def test_baidu_search(page):
    """测试百度搜索页面的基本功能"""
    try:
        # 访问百度首页
        page.goto("https://www.baidu.com", wait_until="networkidle", timeout=30000)
        
        # 等待页面加载完成
        page.wait_for_load_state("domcontentloaded")
        
        # 验证页面标题
        title = page.title()
        assert "百度" in title, f"Expected '百度' in title, but got: {title}"
        
        # 验证搜索框存在
        search_box = page.locator("#kw")
        assert search_box.is_visible(), "Search box should be visible"
        
    except Exception as e:
        # 失败时截图（用于调试）
        page.screenshot(path="test_failure_baidu.png")
        raise e

@pytest.mark.smoke
def test_httpbin_status(page):
    """测试 httpbin.org 状态页面（另一个稳定的测试目标）"""
    try:
        # 访问 httpbin 状态页面
        page.goto("https://httpbin.org/status/200", timeout=20000)
        
        # 验证状态码 200 响应
        # httpbin.org/status/200 会返回一个空页面，这是正常的
        assert page.url.endswith("/status/200"), "Should be on the status/200 page"
        
    except Exception as e:
        # 失败时截图（用于调试）
        page.screenshot(path="test_failure_httpbin.png")
        raise e