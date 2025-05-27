# 开发文档

本文档提供了 Playwright Python Docker 项目的详细开发指南和技术说明。

## 开发环境配置

### 本地开发环境

#### 系统要求

- Python 3.11+
- Docker 20.10+
- Git 2.30+

#### 环境配置步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd playwright-python-docker
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   python -m playwright install
   ```

4. **验证安装**
   ```bash
   pytest tests/test_sample.py -v
   ```

### Docker 开发环境

#### 构建开发镜像

```bash
docker build -t playwright-python-dev .
```

#### 交互式开发

```bash
docker run -it --rm -v $(pwd):/app playwright-python-dev bash
```

#### 运行测试

```bash
docker run --rm -v $(pwd):/app playwright-python-dev pytest -v
```

## 项目架构

### 目录结构详解

```
playwright-python-docker/
├── Dockerfile                 # 生产环境 Docker 镜像
├── requirements.txt           # Python 依赖声明
├── .gitignore                # Git 忽略规则
├── README.md                 # 项目说明文档
├── DEVELOPMENT.md            # 开发文档（本文件）
├── tests/                    # 测试文件目录
│   ├── __init__.py          # Python 包初始化
│   ├── test_sample.py       # 示例测试
│   ├── conftest.py          # pytest 配置（可选）
│   └── utils/               # 测试工具类（可选）
├── .github/                 # GitHub 配置
│   └── workflows/
│       └── docker-pytest.yml  # CI/CD 工作流
└── docs/                    # 文档目录（可选）
```

### 技术架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GitHub Actions │    │   Docker        │    │   Playwright    │
│   CI/CD Pipeline │────│   Container     │────│   Test Runner   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Browser       │
                       │   (Chromium/    │
                       │    Firefox)     │
                       └─────────────────┘
```

## 开发最佳实践

### 测试编写规范

#### 1. 文件命名规范

- 测试文件以 `test_` 开头
- 测试函数以 `test_` 开头
- 使用描述性的名称

```python
# 好的命名
test_user_login_success.py
test_search_functionality.py

def test_user_can_login_with_valid_credentials():
    pass

def test_search_returns_relevant_results():
    pass
```

#### 2. 测试结构模式

使用 AAA (Arrange-Act-Assert) 模式：

```python
def test_example():
    # Arrange - 准备测试数据和环境
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Act - 执行被测试的操作
        page.goto("https://example.com")
        page.click("#login-button")
        page.fill("#username", "testuser")
        page.fill("#password", "testpass")
        page.click("#submit")
        
        # Assert - 验证结果
        assert page.locator(".welcome-message").is_visible()
        assert "Welcome" in page.locator(".welcome-message").text_content()
        
        browser.close()
```

#### 3. 页面对象模式 (Page Object Pattern)

创建页面对象类来封装页面元素和操作：

```python
# pages/login_page.py
class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        self.login_button = page.locator("#login-button")
        self.error_message = page.locator(".error-message")
    
    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
    
    def get_error_message(self):
        return self.error_message.text_content()

# tests/test_login.py
from pages.login_page import LoginPage

def test_login_with_invalid_credentials():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        login_page = LoginPage(page)
        
        page.goto("https://example.com/login")
        login_page.login("invalid", "credentials")
        
        assert "Invalid credentials" in login_page.get_error_message()
        browser.close()
```

### 配置管理

#### pytest 配置文件

创建 `conftest.py` 文件来配置 pytest：

```python
# tests/conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

@pytest.fixture
def base_url():
    return "https://example.com"
```

#### 环境变量配置

```python
# config.py
import os

class Config:
    BASE_URL = os.getenv("BASE_URL", "https://example.com")
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")
    TIMEOUT = int(os.getenv("TIMEOUT", "30000"))
```

### 错误处理和调试

#### 1. 截图和视频录制

```python
def test_with_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            page.goto("https://example.com")
            # 测试操作
            page.click("#button")
        except Exception as e:
            # 失败时截图
            page.screenshot(path="failure_screenshot.png")
            raise e
        finally:
            browser.close()
```

#### 2. 等待策略

```python
# 等待元素出现
page.wait_for_selector("#element", timeout=5000)

# 等待网络请求完成
page.wait_for_load_state("networkidle")

# 等待特定条件
page.wait_for_function("() => document.readyState === 'complete'")
```

#### 3. 调试技巧

```python
# 启用调试模式
browser = p.chromium.launch(headless=False, slow_mo=1000)

# 添加断点
page.pause()

# 打印页面内容
print(page.content())

# 打印元素信息
element = page.locator("#element")
print(f"Element text: {element.text_content()}")
print(f"Element visible: {element.is_visible()}")
```

## Docker 开发

### Dockerfile 优化

当前 Dockerfile 已经进行了以下优化：

1. **多阶段构建**: 减少最终镜像大小
2. **缓存优化**: 合理安排 COPY 和 RUN 指令顺序
3. **依赖清理**: 删除不必要的缓存和临时文件

### 本地 Docker 开发

#### 开发时挂载代码

```bash
# 挂载当前目录到容器
docker run -it --rm -v $(pwd):/app playwright-python-dev bash

# 运行特定测试
docker run --rm -v $(pwd):/app playwright-python-dev pytest tests/test_specific.py -v
```

#### Docker Compose 配置

项目已包含 `docker-compose.yml` 文件，提供多个服务用于不同的开发场景：

```yaml
version: '3.8'
services:
  # 开发环境服务
  playwright-dev:
    build: .
    volumes:
      - .:/app
    working_dir: /app
    environment:
      - HEADLESS=true
      - BROWSER=chromium
    command: bash
    stdin_open: true
    tty: true

  # 测试运行服务
  playwright-test:
    build: .
    volumes:
      - .:/app
    working_dir: /app
    environment:
      - HEADLESS=true
      - BROWSER=chromium
    command: pytest -v

  # 多浏览器测试服务
  test-chromium:
    # Chromium 测试配置
  test-firefox:
    # Firefox 测试配置
```

**常用 Docker Compose 命令：**

```bash
# 构建所有服务
docker-compose build

# 运行测试
docker-compose up playwright-test

# 进入开发环境
docker-compose run playwright-dev

# 运行特定浏览器测试
docker-compose up test-chromium
docker-compose up test-firefox

# 后台运行服务
docker-compose up -d playwright-test

# 查看服务日志
docker-compose logs playwright-test

# 停止并删除容器
docker-compose down

# 重新构建并运行
docker-compose up --build playwright-test
```

## CI/CD 流程

### GitHub Actions 工作流

当前配置的工作流程：

1. **代码检出**: 获取最新代码
2. **Docker 构建**: 构建测试镜像
3. **测试执行**: 在容器中运行测试
4. **结果报告**: 输出测试结果

### 扩展 CI/CD

可以添加的功能：

```yaml
# .github/workflows/extended-ci.yml
name: Extended CI

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install flake8 black
      - run: flake8 tests/
      - run: black --check tests/

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox]
    steps:
      - uses: actions/checkout@v4
      - name: Build and test
        run: |
          docker build -t playwright-test .
          docker run --rm -e BROWSER=${{ matrix.browser }} \
            -v ${{ github.workspace }}:/app -w /app playwright-test pytest -m smoke
```

## 性能优化

### 测试执行优化

1. **并行执行**
   ```bash
   pytest -n auto  # 需要 pytest-xdist
   ```

2. **浏览器复用**
   ```python
   # 在 conftest.py 中配置浏览器复用
   @pytest.fixture(scope="session")
   def browser():
       with sync_playwright() as p:
           browser = p.chromium.launch()
           yield browser
           browser.close()
   ```

3. **选择性测试**
   ```bash
   # 运行特定标记的测试
   pytest -m "smoke"
   
   # 运行特定模块
   pytest tests/test_login.py
   ```

### Docker 镜像优化

1. **使用 .dockerignore**
   ```
   .git
   .github
   __pycache__
   *.pyc
   .pytest_cache
   ```

2. **多阶段构建示例**
   ```dockerfile
   # 构建阶段
   FROM python:3.11-slim as builder
   COPY requirements.txt .
   RUN pip install --user -r requirements.txt
   
   # 运行阶段
   FROM python:3.11-slim
   COPY --from=builder /root/.local /root/.local
   # ... 其他配置
   ```

## 故障排除

### 常见问题及解决方案

#### 1. 浏览器启动失败

```bash
# 检查系统依赖
docker run --rm playwright-python-dev python -m playwright install --dry-run

# 更新浏览器
docker run --rm playwright-python-dev python -m playwright install chromium
```

#### 2. 测试超时

```python
# 增加超时时间
page.set_default_timeout(60000)  # 60秒

# 或在特定操作中设置
page.click("#button", timeout=10000)
```

#### 3. 元素定位失败

```python
# 使用更稳定的定位器
page.locator("text=Login")  # 文本定位
page.locator("[data-testid=login-btn]")  # 测试ID定位

# 等待元素可见
page.wait_for_selector("#element", state="visible")
```

## 代码质量

### 代码规范

使用以下工具保证代码质量：

```bash
# 代码格式化
black tests/

# 代码检查
flake8 tests/

# 类型检查
mypy tests/
```

### 测试覆盖率

```bash
# 安装覆盖率工具
pip install pytest-cov

# 运行带覆盖率的测试
pytest --cov=tests/ --cov-report=html
```

## 扩展功能

### 添加新的测试类型

1. **API 测试集成**
2. **数据库测试**
3. **移动端测试**
4. **性能测试**

### 报告和监控

1. **Allure 报告**
2. **测试结果通知**
3. **性能监控**

## 参考资源

- [Playwright 官方文档](https://playwright.dev/python/)
- [pytest 文档](https://docs.pytest.org/)
- [Docker 最佳实践](https://docs.docker.com/develop/dev-best-practices/)
- [GitHub Actions 文档](https://docs.github.com/en/actions) 