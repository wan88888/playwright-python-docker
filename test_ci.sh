#!/bin/bash

# CI 测试脚本 - 本地验证 GitHub Actions 配置

set -e

echo "🚀 开始本地 CI 测试..."

# 构建 Docker 镜像
echo "📦 构建 Docker 镜像..."
docker build -t playwright-python .

# 运行烟雾测试
echo "🔥 运行烟雾测试..."
docker run --rm \
  -v $(pwd):/app \
  -w /app \
  -e HEADLESS=true \
  -e BROWSER=chromium \
  playwright-python pytest -m smoke -v --tb=short

# 运行所有测试
echo "🧪 运行所有测试..."
docker run --rm \
  -v $(pwd):/app \
  -w /app \
  -e HEADLESS=true \
  -e BROWSER=chromium \
  playwright-python pytest -v --tb=short --maxfail=3

echo "✅ 所有测试通过！"

# 清理
echo "🧹 清理测试产物..."
rm -f test_failure*.png *.log

echo "🎉 本地 CI 测试完成！" 