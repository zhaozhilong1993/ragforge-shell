#!/bin/bash

# 快速测试脚本 - 验证压力测试功能
# 使用方法: ./tests/quick_test.sh

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置
TOTAL_DOCUMENTS=100  # 快速测试只上传100个文档
BATCH_SIZE=10
DATASET_NAME="quick_test_dataset"
LOG_FILE="tests/quick_test.log"
TEMP_DIR="tests/temp_docs_quick"

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
}

# 检查认证状态
check_auth() {
    log_info "检查认证状态..."
    
    if ! uv run python main.py user status &> /dev/null; then
        log_error "用户未登录，请先登录"
        log_info "运行: uv run python main.py user login <email> <password>"
        exit 1
    fi
    
    log_success "认证状态正常"
}

# 创建数据集
create_dataset() {
    log_info "创建数据集: $DATASET_NAME"
    
    # 删除已存在的数据集（如果存在）
    # 由于数据集列表API可能有问题，直接尝试创建新数据集
    log_warning "数据集列表API可能有问题，直接创建新数据集"
    
    # 创建新数据集
    if uv run python main.py datasets create "$DATASET_NAME" --description "快速测试数据集" &> /dev/null; then
        log_success "数据集创建成功"
    else
        log_warning "数据集可能已存在，继续测试"
    fi
}

# 生成测试文档
generate_documents() {
    log_info "生成 $TOTAL_DOCUMENTS 个测试文档..."
    
    mkdir -p "$TEMP_DIR"
    
    # 生成文档内容模板
    cat > "$TEMP_DIR/template.txt" << 'EOF'
# 快速测试文档 {DOC_ID}

## 概述
这是一个用于快速测试的文档，文档ID为 {DOC_ID}。

## 内容
- 文档编号：{DOC_ID}
- 生成时间：{TIMESTAMP}
- 测试类型：快速测试
- 文档大小：约 200 字节

## 测试目标
验证系统的基本功能：
1. 文档上传
2. 数据集管理
3. 系统响应

## 结束语
这是第 {DOC_ID} 个快速测试文档。
EOF
    
    log_success "文档模板创建完成"
}

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
    
    log_info "上传批次 $batch_num: 文档 $start_id 到 $end_id"
    
    local success_count=0
    local fail_count=0
    
    for ((i=start_id; i<=end_id; i++)); do
        local doc_file=$(generate_single_doc $i)
        
        if uv run python main.py documents upload "$DATASET_NAME" --file "$doc_file" &> /dev/null; then
            success_count=$((success_count + 1))
            log_success "文档 $i 上传成功"
        else
            fail_count=$((fail_count + 1))
            log_warning "文档 $i 上传失败"
        fi
    done
    
    log_success "批次 $batch_num 完成: 成功 $success_count, 失败 $fail_count"
    echo "$success_count $fail_count"
}

# 执行快速测试
run_quick_test() {
    log_info "开始快速测试..."
    log_info "目标: 上传 $TOTAL_DOCUMENTS 个文档到数据集 $DATASET_NAME"
    
    total_success=0
    total_fail=0
    start_time=$(date +%s)
    
    # 计算批次数量
    local total_batches=$((TOTAL_DOCUMENTS / BATCH_SIZE))
    if [ $((TOTAL_DOCUMENTS % BATCH_SIZE)) -gt 0 ]; then
        total_batches=$((total_batches + 1))
    fi
    
    log_info "将分 $total_batches 个批次上传，每批次 $BATCH_SIZE 个文档"
    
    # 执行批次上传
    for ((batch=1; batch<=total_batches; batch++)); do
        local start_id=$(((batch-1) * BATCH_SIZE + 1))
        local end_id=$((batch * BATCH_SIZE))
        
        if [ $end_id -gt $TOTAL_DOCUMENTS ]; then
            end_id=$TOTAL_DOCUMENTS
        fi
        
        local result=$(upload_batch $start_id $end_id $batch)
        local batch_success=$(echo $result | cut -d' ' -f1)
        local batch_fail=$(echo $result | cut -d' ' -f2)
        
        total_success=$((total_success + batch_success))
        total_fail=$((total_fail + batch_fail))
    done
    
    end_time=$(date +%s)
    total_time=$((end_time - start_time))
    
    log_success "快速测试完成!"
    log_info "总耗时: $total_time 秒"
    log_info "总成功: $total_success 个文档"
    log_info "总失败: $total_fail 个文档"
    if [ $total_time -gt 0 ]; then
        log_info "平均速率: $((total_success / total_time)) 文档/秒"
    else
        log_info "平均速率: 0 文档/秒"
    fi
    
    if [ $((total_success + total_fail)) -gt 0 ]; then
        log_info "成功率: $((total_success * 100 / (total_success + total_fail)))%"
    else
        log_info "成功率: 0%"
    fi
}

# 验证结果
verify_results() {
    log_info "验证测试结果..."
    
    # 检查数据集中的文档数量
    local doc_count=$(uv run python main.py documents list "$DATASET_NAME" 2>/dev/null | grep -c "文档" || echo "0")
    log_info "数据集中的文档数量: $doc_count"
    
    # 显示数据集信息
    echo "=== 数据集信息 ===" | tee -a "$LOG_FILE"
    uv run python main.py datasets show "$DATASET_NAME" | tee -a "$LOG_FILE"
    
    # 显示文档列表（前10个）
    echo "=== 文档列表（前10个）===" | tee -a "$LOG_FILE"
    uv run python main.py documents list "$DATASET_NAME" | head -20 | tee -a "$LOG_FILE"
}

# 清理临时文件
cleanup() {
    log_info "清理临时文件..."
    rm -rf "$TEMP_DIR"
    log_success "清理完成"
}

# 主函数
main() {
    log_info "开始快速测试脚本"
    log_info "日志文件: $LOG_FILE"
    
    # 创建日志文件
    echo "=== 快速测试日志 $(date) ===" > "$LOG_FILE"
    
    # 执行测试步骤
    check_auth
    create_dataset
    generate_documents
    run_quick_test
    verify_results
    cleanup
    
    log_success "快速测试脚本执行完成!"
    log_info "详细日志请查看: $LOG_FILE"
}

# 信号处理
trap cleanup EXIT

# 执行主函数
main "$@" 