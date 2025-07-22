#!/bin/bash

# 压力测试脚本 - 测试10万个文档的系统稳定性
# 使用方法: ./tests/stress_test.sh

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
TOTAL_DOCUMENTS=100000
BATCH_SIZE=100
DATASET_NAME="stress_test_dataset"
LOG_FILE="stress_test.log"
TEMP_DIR="tests/temp_docs"

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

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    if ! command -v python &> /dev/null; then
        log_error "Python 未安装"
        exit 1
    fi
    
    if ! command -v uv &> /dev/null; then
        log_error "uv 未安装"
        exit 1
    fi
    
    log_success "依赖检查通过"
}

# 检查认证状态
check_auth() {
    log_info "检查认证状态..."
    
    # 获取脚本所在目录的上级目录（项目根目录）
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
    
    if ! uv run python "$PROJECT_ROOT/main.py" user status &> /dev/null; then
        log_error "用户未登录，请先登录"
        log_info "运行: uv run python main.py user login <email> <password>"
        exit 1
    fi
    
    log_success "认证状态正常"
}

# 创建数据集
create_dataset() {
    log_info "创建数据集: $DATASET_NAME"
    
    # 创建数据集并获取ID
    RESPONSE=$(uv run python "$PROJECT_ROOT/main.py" datasets create "$DATASET_NAME" --description "压力测试数据集" --format json 2>/dev/null)
    
    # 提取数据集ID
    DATASET_ID=$(echo "$RESPONSE" | grep -o '"id": "[^"]*"' | cut -d'"' -f4)
    
    if [ -z "$DATASET_ID" ]; then
        log_warning "无法获取数据集ID，使用数据集名称"
        DATASET_ID="$DATASET_NAME"
    else
        log_success "数据集创建成功，ID: $DATASET_ID"
    fi
    
    # 设置全局变量
    export DATASET_ID
}

# 生成测试文档
generate_documents() {
    log_info "生成 $TOTAL_DOCUMENTS 个测试文档..."
    
    mkdir -p "$TEMP_DIR"
    
    # 生成文档内容模板
    cat > "$TEMP_DIR/template.txt" << 'EOF'
# 测试文档 {DOC_ID}

## 概述
这是一个用于压力测试的文档，文档ID为 {DOC_ID}。

## 内容
本文档包含以下内容：
- 文档编号：{DOC_ID}
- 生成时间：{TIMESTAMP}
- 测试类型：压力测试
- 文档大小：约 500 字节

## 详细信息
这是一个模拟真实文档的测试文件，用于验证系统在处理大量文档时的稳定性。文档包含各种格式的内容，包括标题、列表、段落等。

## 技术参数
- 文档类型：Markdown
- 编码格式：UTF-8
- 行数：约 20 行
- 字符数：约 500 字符

## 测试目标
通过批量上传大量文档来测试系统的：
1. 存储性能
2. 处理能力
3. 响应时间
4. 错误处理
5. 资源使用情况

## 结束语
这是第 {DOC_ID} 个测试文档，用于验证系统在极端负载下的表现。
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
    start_id=$1
    end_id=$2
    batch_num=$3
    
    log_info "上传批次 $batch_num: 文档 $start_id 到 $end_id"
    
    success_count=0
    fail_count=0
    
    for ((i=start_id; i<=end_id; i++)); do
        doc_file=$(generate_single_doc $i)
        
        if uv run python "$PROJECT_ROOT/main.py" documents upload "$DATASET_ID" --file "$doc_file" &> /dev/null; then
            success_count=$((success_count + 1))
        else
            fail_count=$((fail_count + 1))
            log_warning "文档 $i 上传失败"
        fi
        
        # 每100个文档显示一次进度
        if ((i % 100 == 0)); then
            log_info "进度: $i/$TOTAL_DOCUMENTS (成功: $success_count, 失败: $fail_count)"
        fi
    done
    
    log_success "批次 $batch_num 完成: 成功 $success_count, 失败 $fail_count"
    echo "$success_count $fail_count"
}

# 执行压力测试
run_stress_test() {
    log_info "开始压力测试..."
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
        
        # 每10个批次显示一次总体进度
        if [ $((batch % 10)) -eq 0 ]; then
            local elapsed=$(( $(date +%s) - start_time ))
            local rate=0
            if [ $elapsed -gt 0 ]; then
                rate=$((total_success / elapsed))
            fi
            local success_rate=0
            if [ $((total_success + total_fail)) -gt 0 ]; then
                success_rate=$((total_success * 100 / (total_success + total_fail)))
            fi
            log_info "总体进度: $((batch * BATCH_SIZE))/$TOTAL_DOCUMENTS, 成功率: ${success_rate}%, 速率: $rate 文档/秒"
        fi
    done
    
    end_time=$(date +%s)
    total_time=$((end_time - start_time))
    
    log_success "压力测试完成!"
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

# 清理临时文件
cleanup() {
    log_info "清理临时文件..."
    rm -rf "$TEMP_DIR"
    log_success "清理完成"
}

# 显示系统状态
show_system_status() {
    log_info "检查系统状态..."
    
    echo "=== 系统状态 ===" | tee -a "$LOG_FILE"
    uv run python "$PROJECT_ROOT/main.py" system status | tee -a "$LOG_FILE"
    
    echo "=== 数据集状态 ===" | tee -a "$LOG_FILE"
    uv run python "$PROJECT_ROOT/main.py" datasets list | tee -a "$LOG_FILE"
    
    echo "=== 用户状态 ===" | tee -a "$LOG_FILE"
    uv run python "$PROJECT_ROOT/main.py" user status | tee -a "$LOG_FILE"
}

# 主函数
main() {
    log_info "开始压力测试脚本"
    log_info "日志文件: $LOG_FILE"
    
    # 创建日志文件
    echo "=== 压力测试日志 $(date) ===" > "$LOG_FILE"
    
    # 执行测试步骤
    check_dependencies
    check_auth
    create_dataset
    generate_documents
    run_stress_test
    show_system_status
    cleanup
    
    log_success "压力测试脚本执行完成!"
    log_info "详细日志请查看: $LOG_FILE"
}

# 信号处理
trap cleanup EXIT

# 执行主函数
main "$@" 