# Playwright Python Docker 自动化测试项目

这是一个基于 Playwright 和 Python 的 Web 自动化测试项目，使用 Docker 进行容器化部署，支持在隔离环境中运行浏览器自动化测试。

## 项目特性

- 🚀 基于 Playwright 的现代化 Web 自动化测试
- 🐍 使用 Python 编写测试脚本
- 🐳 Docker 容器化部署，环境一致性保证
- 🌐 支持多浏览器测试（Chromium、Firefox）
- ⚡ GitHub Actions 自动化 CI/CD 流程
- 📦 轻量级依赖管理

## 技术栈

- **Python 3.11**: 主要编程语言
- **Playwright**: Web 自动化测试框架
- **pytest**: 测试运行器
- **Docker**: 容器化部署
- **GitHub Actions**: 持续集成

## 项目结构

```
playwright-python-docker/
├── Dockerfile              # Docker 镜像构建文件
├── docker-compose.yml      # Docker Compose 配置文件
├── requirements.txt         # Python 依赖包
├── .gitignore              # Git 忽略文件
├── .dockerignore           # Docker 构建忽略文件
├── README.md               # 项目说明文档
├── DEVELOPMENT.md          # 详细开发文档
├── tests/                  # 测试文件目录
│   ├── conftest.py         # pytest 配置和 fixtures
│   └── test_sample.py      # 示例测试文件
├── pytest.ini             # pytest 配置文件
└── .github/                # GitHub Actions 配置
    └── workflows/
        └── docker-pytest.yml  # CI/CD 工作流
```

## 快速开始

### 方式一：使用 Docker（推荐）

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd playwright-python-docker
   ```

2. **构建 Docker 镜像**
   ```bash
   docker build -t playwright-python .
   ```

3. **运行测试**
   ```bash
   docker run --rm -v $(pwd):/app playwright-python pytest
   ```

### 方式二：使用 Docker Compose（推荐用于开发）

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd playwright-python-docker
   ```

2. **运行测试**
   ```bash
   # 运行所有测试
   docker-compose up playwright-test

   # 运行 Chromium 测试
   docker-compose up test-chromium

   # 运行 Firefox 测试
   docker-compose up test-firefox
   ```

3. **进入开发环境**
   ```bash
   docker-compose run playwright-dev
   ```

### 方式三：本地环境

1. **安装 Python 依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **安装 Playwright 浏览器**
   ```bash
   python -m playwright install
   ```

3. **运行测试**
   ```bash
   pytest
   ```

## 测试示例

项目包含多个示例测试 `tests/test_sample.py`，演示如何使用 Playwright 进行 Web 自动化测试：

### 稳定的烟雾测试
```python
@pytest.mark.smoke
def test_example_com(page):
    """测试 example.com 网站（稳定的测试目标）"""
    page.goto("https://example.com", wait_until="networkidle")
    title = page.title()
    assert "Example Domain" in title
```

### 集成测试
```python
@pytest.mark.integration
def test_baidu_search(page):
    """测试百度搜索页面的基本功能"""
    page.goto("https://www.baidu.com", wait_until="networkidle", timeout=30000)
    assert "百度" in page.title()
    search_box = page.locator("#kw")
    assert search_box.is_visible()
```

### 运行特定类型的测试
```bash
# 只运行烟雾测试（快速验证）
pytest -m smoke

# 只运行集成测试
pytest -m integration

# 运行所有测试
pytest
```

## 编写新测试

1. 在 `tests/` 目录下创建新的测试文件
2. 文件名以 `test_` 开头
3. 使用 Playwright API 编写测试逻辑
4. 运行 `pytest` 执行测试

### 测试示例模板

```python
import pytest
from playwright.sync_api import sync_playwright

def test_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 访问页面
        page.goto("https://example.com")
        
        # 执行操作
        page.click("button")
        page.fill("input", "test")
        
        # 断言验证
        assert page.locator("h1").text_content() == "Expected Title"
        
        browser.close()
```

## Docker 镜像说明

Docker 镜像基于 `python:3.11-slim`，包含：

- Python 3.11 运行环境
- Playwright 及其浏览器依赖
- Chromium 和 Firefox 浏览器
- 必要的系统依赖包

镜像大小经过优化，移除了不必要的缓存和临时文件。

## CI/CD 流程

项目配置了 GitHub Actions 自动化流程：

- **触发条件**: 推送到 main 分支或创建 Pull Request
- **执行步骤**:
  1. 检出代码
  2. 设置 Docker Buildx
  3. 构建 Docker 镜像
  4. 在容器中运行测试

## 开发指南

### 使用 Docker Compose 进行开发

项目提供了 `docker-compose.yml` 文件来简化开发流程：

```bash
# 进入交互式开发环境
docker-compose run playwright-dev

# 运行特定测试文件
docker-compose run playwright-test pytest tests/test_sample.py -v

# 在后台运行测试
docker-compose up -d playwright-test

# 查看测试日志
docker-compose logs playwright-test

# 停止所有服务
docker-compose down
```

### 添加新依赖

1. 在 `requirements.txt` 中添加依赖包
2. 重新构建 Docker 镜像：
   ```bash
   docker-compose build
   ```

### 调试测试

使用 Docker Compose 进行调试：

```bash
# 进入交互式开发环境
docker-compose run playwright-dev

# 或使用传统 Docker 命令
docker run -it --rm -v $(pwd):/app playwright-python bash
```

### 本地验证 CI 配置

项目提供了一个测试脚本来本地验证 GitHub Actions 配置：

```bash
# 运行本地 CI 测试
./test_ci.sh

# 或手动执行步骤
chmod +x test_ci.sh
./test_ci.sh
```

### 浏览器选项

支持的浏览器：
- `chromium` (默认)
- `firefox`
- `webkit` (需要额外配置)

## 常见问题

### Q: 测试运行缓慢？
A: 可以使用 `headless=True` 模式运行浏览器，或者并行运行测试。

### Q: 如何查看测试运行过程？
A: 设置 `headless=False` 并使用本地环境运行，或者添加截图功能。

### Q: Docker 容器中无法显示浏览器界面？
A: Docker 环境默认为 headless 模式，这是正常的。如需查看界面，请使用本地环境。

### Q: 如何使用 Docker Compose 运行特定的测试？
A: 可以使用以下命令：
```bash
# 运行特定测试文件
docker-compose run playwright-test pytest tests/test_sample.py -v

# 运行带标记的测试
docker-compose run playwright-test pytest -m "smoke" -v

# 使用不同浏览器运行测试
docker-compose up test-firefox
```

### Q: 遇到 TimeoutError 怎么办？
A: 超时错误通常由网络问题或页面加载缓慢引起，可以尝试：
```bash
# 只运行稳定的烟雾测试
pytest -m smoke

# 增加超时时间
docker-compose run playwright-test pytest --timeout=600

# 使用本地环境测试网络连接
ping example.com
```
建议优先运行 `example.com` 等稳定网站的测试，避免依赖可能不稳定的外部服务。

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。

## 联系方式

如有问题或建议，请创建 Issue 或联系项目维护者。 