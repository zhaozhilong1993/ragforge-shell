#!/bin/bash

# 最小化测试脚本
set -e

echo "开始最小化测试"

# 检查认证状态
echo "检查认证状态..."
if uv run python main.py user status &> /dev/null; then
    echo "认证状态正常"
else
    echo "用户未登录"
    exit 1
fi

# 创建数据集
echo "创建测试数据集..."
if uv run python main.py datasets create "mini_test_dataset" --description "最小化测试数据集" &> /dev/null; then
    echo "数据集创建成功"
else
    echo "数据集可能已存在，继续测试"
fi

# 生成测试文档
echo "生成测试文档..."
mkdir -p tests/temp_mini

cat > tests/temp_mini/test_doc.txt << 'EOF'
# 测试文档

这是一个用于测试的文档。

## 内容
- 文档类型：测试文档
- 生成时间：$(date)
- 测试目标：验证上传功能

## 结束语
这是一个最小化的测试文档。
EOF

echo "测试文档生成完成"

# 上传文档
echo "上传测试文档..."
if uv run python main.py documents upload "mini_test_dataset" --file "tests/temp_mini/test_doc.txt" &> /dev/null; then
    echo "文档上传成功"
else
    echo "文档上传失败"
    exit 1
fi

# 清理
echo "清理临时文件..."
rm -rf tests/temp_mini

echo "最小化测试完成" 