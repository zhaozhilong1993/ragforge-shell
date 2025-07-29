#!/bin/bash

# RAGForge Shell 卸载脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 卸载ragforge命令
uninstall_command() {
    print_info "卸载ragforge命令..."
    
    if command -v ragforge &> /dev/null; then
        if command -v sudo &> /dev/null; then
            sudo rm -f /usr/local/bin/ragforge
        else
            rm -f /usr/local/bin/ragforge
        fi
        print_success "ragforge命令已卸载"
    else
        print_warning "ragforge命令未找到"
    fi
}

# 清理虚拟环境
cleanup_venv() {
    print_info "清理虚拟环境..."
    
    if [ -d ".venv" ]; then
        rm -rf .venv
        print_success "虚拟环境已清理"
    else
        print_warning "虚拟环境不存在"
    fi
}

# 清理缓存文件
cleanup_cache() {
    print_info "清理缓存文件..."
    
    # 清理Python缓存
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    print_success "缓存文件已清理"
}

# 显示卸载完成信息
show_completion() {
    print_success "卸载完成！"
    echo
    echo "已清理的内容："
    echo "  - ragforge命令"
    echo "  - 虚拟环境"
    echo "  - 缓存文件"
    echo
    echo "注意：配置文件 config.yaml 和项目文件未删除"
    echo "如需完全删除，请手动删除整个目录"
}

# 主卸载流程
main() {
    echo "=========================================="
    echo "    RAGForge Shell 卸载脚本"
    echo "=========================================="
    echo
    
    # 确认卸载
    read -p "确定要卸载RAGForge Shell吗？(y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "取消卸载"
        exit 0
    fi
    
    uninstall_command
    cleanup_venv
    cleanup_cache
    show_completion
}

# 运行主函数
main "$@" 