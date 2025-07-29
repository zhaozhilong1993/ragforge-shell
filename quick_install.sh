#!/bin/bash

# RAGForge Shell 快速安装脚本
# 支持一键安装，无需交互

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

# 检查系统要求
check_requirements() {
    print_info "检查系统要求..."
    
    # 检查Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装"
        exit 1
    fi
    
    # 检查pip
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 未安装"
        exit 1
    fi
    
    print_success "系统要求检查通过"
}

# 安装依赖
install_dependencies() {
    print_info "安装Python依赖..."
    
    cd "$(dirname "$0")"
    
    # 创建虚拟环境
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        print_success "虚拟环境创建完成"
    fi
    
    # 激活虚拟环境并安装依赖
    source .venv/bin/activate
    pip install -r requirements.txt
    print_success "依赖安装完成"
}

# 创建ragforge命令
create_command() {
    print_info "创建ragforge命令..."
    
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    
    # 创建ragforge命令脚本
    cat > /tmp/ragforge << 'EOF'
#!/bin/bash

# RAGForge 命令行工具
SCRIPT_DIR="SCRIPT_DIR_PLACEHOLDER"

# 检查虚拟环境是否存在
if [ -d "$SCRIPT_DIR/.venv" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
    python "$SCRIPT_DIR/main.py" "$@"
else
    python3 "$SCRIPT_DIR/main.py" "$@"
fi
EOF

    # 替换占位符
    sed -i.bak "s|SCRIPT_DIR_PLACEHOLDER|$SCRIPT_DIR|g" /tmp/ragforge
    rm -f /tmp/ragforge.bak
    
    chmod +x /tmp/ragforge
    
    # 安装到系统路径
    if command -v sudo &> /dev/null; then
        sudo mv /tmp/ragforge /usr/local/bin/ragforge
    else
        mv /tmp/ragforge /usr/local/bin/ragforge
    fi
    
    print_success "ragforge命令已安装"
}

# 创建配置文件
create_config() {
    print_info "创建配置文件..."
    
    if [ ! -f "config.yaml" ]; then
        cat > config.yaml << EOF
# RAGForge API 配置
api:
  base_url: "http://localhost:9380"
  timeout: 30
  retries: 3

# 认证配置
auth:
  username: ""
  password: ""
  api_key: ""

# 输出配置
output:
  format: "table"
  colors: true
  verbose: false

# 调试配置
debug:
  enabled: false
  level: "INFO"
EOF
        print_success "配置文件已创建"
    fi
}

# 验证安装
verify_installation() {
    print_info "验证安装..."
    
    if command -v ragforge &> /dev/null; then
        ragforge version > /dev/null 2>&1
        print_success "安装验证成功"
    else
        print_error "安装验证失败"
        exit 1
    fi
}

# 显示安装完成信息
show_completion() {
    print_success "安装完成！"
    echo
    echo "使用方法："
    echo "  ragforge --help"
    echo "  ragforge user login"
    echo "  ragforge datasets list"
    echo
    echo "配置文件: $(pwd)/config.yaml"
    echo "请修改配置文件中的base_url为你的RAGForge服务器地址"
}

# 主函数
main() {
    echo "=========================================="
    echo "    RAGForge Shell 快速安装"
    echo "=========================================="
    echo
    
    check_requirements
    install_dependencies
    create_command
    create_config
    verify_installation
    show_completion
}

# 运行主函数
main "$@" 