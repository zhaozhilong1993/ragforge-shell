#!/bin/bash

# 基础测试脚本 - 只测试单个文档上传
set -e

echo "开始基础测试"

# 获取脚本所在目录的上级目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 检查认证状态
echo "检查认证状态..."
if uv run python "$PROJECT_ROOT/main.py" user status &> /dev/null; then
    echo "认证状态正常"
else
    echo "用户未登录"
    exit 1
fi

# 创建数据集
echo "创建测试数据集..."
if uv run python "$PROJECT_ROOT/main.py" datasets create "basic_test_dataset" --description "基础测试数据集" &> /dev/null; then
    echo "数据集创建成功"
else
    echo "数据集可能已存在，继续测试"
fi

# 生成测试文档
echo "生成测试文档..."
mkdir -p temp_basic

cat > temp_basic/test_doc.txt << 'EOF'
# 基础测试文档

这是一个用于基础测试的文档。

## 内容
- 文档类型：基础测试文档
- 生成时间：$(date)
- 测试目标：验证基本上传功能

## 结束语
这是一个基础测试文档。
EOF

echo "测试文档生成完成"

# 上传文档
echo "上传测试文档..."
if uv run python "$PROJECT_ROOT/main.py" documents upload "basic_test_dataset" --file "temp_basic/test_doc.txt" &> /dev/null; then
    echo "文档上传成功"
else
    echo "文档上传失败"
    exit 1
fi

# 清理
echo "清理临时文件..."
rm -rf temp_basic

echo "基础测试完成" 