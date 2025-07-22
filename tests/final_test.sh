#!/bin/bash

# 最终测试脚本 - 使用最简单的逻辑
set -e

echo "开始最终测试"

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
DATASET_NAME="final_test_dataset"

# 创建数据集并获取ID
RESPONSE=$(uv run python "$PROJECT_ROOT/main.py" datasets create "$DATASET_NAME" --description "最终测试数据集" --format json 2>/dev/null)

# 提取数据集ID
DATASET_ID=$(echo "$RESPONSE" | grep -o '"id": "[^"]*"' | cut -d'"' -f4)

if [ -z "$DATASET_ID" ]; then
    echo "无法获取数据集ID，使用数据集名称"
    DATASET_ID="$DATASET_NAME"
else
    echo "数据集创建成功，ID: $DATASET_ID"
fi

# 生成测试文档
echo "生成测试文档..."
mkdir -p temp_final

# 生成10个测试文档
for i in {1..10}; do
    cat > "temp_final/doc_${i}.txt" << EOF
# 最终测试文档 ${i}

这是一个用于最终测试的文档，编号为 ${i}。

## 内容
- 文档编号：${i}
- 生成时间：$(date)
- 测试目标：验证批量上传功能

## 结束语
这是第 ${i} 个最终测试文档。
EOF
done

echo "测试文档生成完成"

# 批量上传文档
echo "批量上传文档..."
success_count=0
fail_count=0

for i in {1..10}; do
    echo "上传文档 ${i}..."
    if uv run python "$PROJECT_ROOT/main.py" documents upload "$DATASET_ID" --file "temp_final/doc_${i}.txt" &> /dev/null; then
        echo "文档 ${i} 上传成功"
        success_count=$((success_count + 1))
    else
        echo "文档 ${i} 上传失败"
        fail_count=$((fail_count + 1))
    fi
done

echo "批量上传完成"
echo "成功: ${success_count} 个文档"
echo "失败: ${fail_count} 个文档"

# 清理
echo "清理临时文件..."
rm -rf temp_final

echo "最终测试完成" 