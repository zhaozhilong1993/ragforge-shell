#!/bin/bash

# 小规模压力测试脚本 - 测试1000个文档
set -e

echo "开始小规模压力测试"

# 获取脚本所在目录的上级目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 配置
TOTAL_DOCUMENTS=1000
BATCH_SIZE=50
DATASET_NAME="small_stress_test_dataset"
TEMP_DIR="temp_small_stress"

# 检查认证状态
echo "检查认证状态..."
if uv run python "$PROJECT_ROOT/main.py" user status &> /dev/null; then
    echo "认证状态正常"
else
    echo "用户未登录"
    exit 1
fi

# 创建数据集
echo "创建数据集: $DATASET_NAME"

# 创建数据集并获取ID
RESPONSE=$(uv run python "$PROJECT_ROOT/main.py" datasets create "$DATASET_NAME" --description "小规模压力测试数据集" --format json 2>/dev/null)

# 提取数据集ID
DATASET_ID=$(echo "$RESPONSE" | grep -o '"id": "[^"]*"' | cut -d'"' -f4)

if [ -z "$DATASET_ID" ]; then
    echo "无法获取数据集ID，使用数据集名称"
    DATASET_ID="$DATASET_NAME"
else
    echo "数据集创建成功，ID: $DATASET_ID"
fi

# 生成测试文档
echo "生成 $TOTAL_DOCUMENTS 个测试文档..."
mkdir -p "$TEMP_DIR"

# 生成文档内容模板
cat > "$TEMP_DIR/template.txt" << 'EOF'
# 小规模压力测试文档 {DOC_ID}

## 概述
这是一个用于小规模压力测试的文档，文档ID为 {DOC_ID}。

## 内容
- 文档编号：{DOC_ID}
- 生成时间：{TIMESTAMP}
- 测试类型：小规模压力测试
- 文档大小：约 300 字节

## 详细信息
这是一个模拟真实文档的测试文件，用于验证系统在处理大量文档时的稳定性。

## 结束语
这是第 {DOC_ID} 个小规模压力测试文档。
EOF

echo "文档模板创建完成"

# 生成单个文档
generate_single_doc() {
    local doc_id=$1
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local filename="$TEMP_DIR/doc_${doc_id}.txt"
    
    # 使用模板生成文档
    sed "s/{DOC_ID}/$doc_id/g; s/{TIMESTAMP}/$timestamp/g" "$TEMP_DIR/template.txt" > "$filename"
    
    echo "$filename"
}

# 上传文档批次
upload_batch() {
    local start_id=$1
    local end_id=$2
    local batch_num=$3
    
    echo "Upload batch $batch_num: documents $start_id to $end_id"
    
    local success_count=0
    local fail_count=0
    
    for ((i=start_id; i<=end_id; i++)); do
        local doc_file=$(generate_single_doc $i)
        
        if uv run python "$PROJECT_ROOT/main.py" documents upload "$DATASET_ID" --file "$doc_file" &> /dev/null; then
            success_count=$((success_count + 1))
        else
            fail_count=$((fail_count + 1))
        fi
        
        # 每50个文档显示一次进度
        if [ $((i % 50)) -eq 0 ]; then
            echo "Progress: $i/$TOTAL_DOCUMENTS (success: $success_count, fail: $fail_count)"
        fi
    done
    
    echo "Batch $batch_num complete: success $success_count, fail $fail_count"
    echo "$success_count $fail_count"
}

# 执行小规模压力测试
echo "开始小规模压力测试..."
echo "目标: 上传 $TOTAL_DOCUMENTS 个文档到数据集 $DATASET_NAME"

total_success=0
total_fail=0
start_time=$(date +%s)

# 计算批次数量
total_batches=$((TOTAL_DOCUMENTS / BATCH_SIZE))
if [ $((TOTAL_DOCUMENTS % BATCH_SIZE)) -gt 0 ]; then
    total_batches=$((total_batches + 1))
fi

echo "将分 $total_batches 个批次上传，每批次 $BATCH_SIZE 个文档"

# 执行批次上传
for ((batch=1; batch<=total_batches; batch++)); do
    start_id=$(((batch-1) * BATCH_SIZE + 1))
    end_id=$((batch * BATCH_SIZE))
    
    if [ $end_id -gt $TOTAL_DOCUMENTS ]; then
        end_id=$TOTAL_DOCUMENTS
    fi
    
    result=$(upload_batch $start_id $end_id $batch)
    batch_success=$(echo $result | cut -d' ' -f1)
    batch_fail=$(echo $result | cut -d' ' -f2)
    
    # 确保变量是数字
    batch_success=${batch_success:-0}
    batch_fail=${batch_fail:-0}
    
    total_success=$((total_success + batch_success))
    total_fail=$((total_fail + batch_fail))
    
    # 每5个批次显示一次总体进度
    if [ $((batch % 5)) -eq 0 ]; then
        elapsed=$(( $(date +%s) - start_time ))
        rate=0
        if [ $elapsed -gt 0 ]; then
            rate=$((total_success / elapsed))
        fi
        success_rate=0
        if [ $((total_success + total_fail)) -gt 0 ]; then
            success_rate=$((total_success * 100 / (total_success + total_fail)))
        fi
        echo "总体进度: $((batch * BATCH_SIZE))/$TOTAL_DOCUMENTS, 成功率: ${success_rate}%, 速率: $rate 文档/秒"
    fi
done

end_time=$(date +%s)
total_time=$((end_time - start_time))

echo "小规模压力测试完成!"
echo "总耗时: $total_time 秒"
echo "总成功: $total_success 个文档"
echo "总失败: $total_fail 个文档"
if [ $total_time -gt 0 ]; then
    echo "平均速率: $((total_success / total_time)) 文档/秒"
else
    echo "平均速率: 0 文档/秒"
fi
if [ $((total_success + total_fail)) -gt 0 ]; then
    echo "成功率: $((total_success * 100 / (total_success + total_fail)))%"
else
    echo "成功率: 0%"
fi

# 清理临时文件
echo "清理临时文件..."
rm -rf "$TEMP_DIR"

echo "小规模压力测试完成" 