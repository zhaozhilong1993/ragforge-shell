#!/bin/bash

# 简单上传测试脚本
set -e

echo "开始简单上传测试"

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
if uv run python "$PROJECT_ROOT/main.py" datasets create "simple_upload_test" --description "简单上传测试数据集" &> /dev/null; then
    echo "数据集创建成功"
else
    echo "数据集可能已存在，继续测试"
fi

# 生成测试文档
echo "生成测试文档..."
mkdir -p temp_simple

cat > temp_simple/test_doc.txt << 'EOF'
# 测试文档

这是一个用于测试的文档。

## 内容
- 文档类型：测试文档
- 生成时间：$(date)
- 测试目标：验证上传功能

## 结束语
这是一个简单的测试文档。
EOF

echo "测试文档生成完成"

# 上传文档
echo "上传测试文档..."
if uv run python "$PROJECT_ROOT/main.py" documents upload "simple_upload_test" --file "temp_simple/test_doc.txt" &> /dev/null; then
    echo "文档上传成功"
else
    echo "文档上传失败"
    exit 1
fi

# 清理
echo "清理临时文件..."
rm -rf temp_simple

echo "简单上传测试完成" 