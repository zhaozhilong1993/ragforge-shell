#!/bin/bash

# 简化测试脚本
set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[INFO]${NC} 开始简化测试"

# 检查认证状态
echo -e "${BLUE}[INFO]${NC} 检查认证状态..."
if uv run python main.py user status &> /dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} 认证状态正常"
else
    echo -e "${RED}[ERROR]${NC} 用户未登录"
    exit 1
fi

# 创建数据集
echo -e "${BLUE}[INFO]${NC} 创建测试数据集..."
if uv run python main.py datasets create "simple_test_dataset" --description "简化测试数据集" &> /dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} 数据集创建成功"
else
    echo -e "${RED}[ERROR]${NC} 数据集创建失败"
    exit 1
fi

# 生成测试文档
echo -e "${BLUE}[INFO]${NC} 生成测试文档..."
mkdir -p tests/temp_simple

cat > tests/temp_simple/test_doc.txt << 'EOF'
# 测试文档

这是一个用于测试的文档。

## 内容
- 文档类型：测试文档
- 生成时间：$(date)
- 测试目标：验证上传功能

## 结束语
这是一个简化的测试文档。
EOF

echo -e "${GREEN}[SUCCESS]${NC} 测试文档生成完成"

# 上传文档
echo -e "${BLUE}[INFO]${NC} 上传测试文档..."
if uv run python main.py documents upload "simple_test_dataset" --file "tests/temp_simple/test_doc.txt" &> /dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} 文档上传成功"
else
    echo -e "${RED}[ERROR]${NC} 文档上传失败"
    exit 1
fi

# 验证结果
echo -e "${BLUE}[INFO]${NC} 验证结果..."
echo "=== 数据集信息 ==="
uv run python main.py datasets show "simple_test_dataset"

echo "=== 文档列表 ==="
uv run python main.py documents list "simple_test_dataset"

# 清理
echo -e "${BLUE}[INFO]${NC} 清理临时文件..."
rm -rf tests/temp_simple

echo -e "${GREEN}[SUCCESS]${NC} 简化测试完成" 