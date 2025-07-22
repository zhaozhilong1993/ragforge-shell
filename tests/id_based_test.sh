#!/bin/bash

# 基于数据集ID的测试脚本
set -e

echo "开始基于数据集ID的测试"

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

# 创建数据集并获取ID
echo "创建测试数据集..."
DATASET_NAME="id_based_test_dataset"

# 创建数据集并获取响应
RESPONSE=$(uv run python "$PROJECT_ROOT/main.py" datasets create "$DATASET_NAME" --description "基于ID的测试数据集" --format json 2>/dev/null)

# 提取数据集ID
DATASET_ID=$(echo "$RESPONSE" | grep -o '"id": "[^"]*"' | cut -d'"' -f4)

if [ -z "$DATASET_ID" ]; then
    echo "无法获取数据集ID，尝试使用数据集名称"
    DATASET_ID="$DATASET_NAME"
fi

echo "数据集ID: $DATASET_ID"

# 生成测试文档
echo "生成测试文档..."
mkdir -p temp_id_based

cat > temp_id_based/test_doc.txt << 'EOF'
# 基于ID的测试文档

这是一个用于基于ID测试的文档。

## 内容
- 文档类型：基于ID的测试文档
- 生成时间：$(date)
- 测试目标：验证使用数据集ID上传功能

## 结束语
这是一个基于ID的测试文档。
EOF

echo "测试文档生成完成"

# 上传文档
echo "上传测试文档..."
if uv run python "$PROJECT_ROOT/main.py" documents upload "$DATASET_ID" --file "temp_id_based/test_doc.txt" &> /dev/null; then
    echo "文档上传成功"
else
    echo "文档上传失败"
    exit 1
fi

# 清理
echo "清理临时文件..."
rm -rf temp_id_based
rm -f test_doc.txt

echo "基于数据集ID的测试完成" 