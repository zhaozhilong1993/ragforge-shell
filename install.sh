#!/bin/bash

# RAGForge Shell 安装脚本
# 安装完成后可以直接使用 ragforge 命令

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

# 检查Python版本
check_python() {
    print_info "检查Python版本..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 未安装，请先安装Python3"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python版本: $PYTHON_VERSION"
}

# 检查pip
check_pip() {
    print_info "检查pip..."
    
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 未安装，请先安装pip3"
        exit 1
    fi
    
    print_success "pip3 已安装"
}

# 安装依赖
install_dependencies() {
    print_info "安装Python依赖..."
    
    cd "$(dirname "$0")"
    
    if [ -f "requirements.txt" ]; then
        pip3 install -r requirements.txt
        print_success "Python依赖安装完成"
    else
        print_error "requirements.txt 文件不存在"
        exit 1
    fi
}

# 创建虚拟环境（可选）
create_venv() {
    print_info "创建虚拟环境..."
    
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        print_success "虚拟环境创建完成"
    else
        print_warning "虚拟环境已存在"
    fi
    
    # 激活虚拟环境
    source .venv/bin/activate
    
    # 在虚拟环境中安装依赖
    pip install -r requirements.txt
    print_success "虚拟环境依赖安装完成"
}

# 创建ragforge命令
create_command() {
    print_info "创建ragforge命令..."
    
    # 获取当前目录的绝对路径
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
    
    # 创建ragforge命令脚本
    cat > /tmp/ragforge << EOF
#!/bin/bash

# RAGForge 命令行工具
# 自动激活虚拟环境并运行命令

SCRIPT_DIR="$SCRIPT_DIR"

# 检查虚拟环境是否存在
if [ -d "\$SCRIPT_DIR/.venv" ]; then
    # 使用虚拟环境
    source "\$SCRIPT_DIR/.venv/bin/activate"
    python "\$SCRIPT_DIR/main.py" "\$@"
else
    # 直接使用系统Python
    python3 "\$SCRIPT_DIR/main.py" "\$@"
fi
EOF

    # 设置执行权限
    chmod +x /tmp/ragforge
    
    # 安装到系统路径
    if command -v sudo &> /dev/null; then
        sudo mv /tmp/ragforge /usr/local/bin/ragforge
    else
        mv /tmp/ragforge /usr/local/bin/ragforge
    fi
    
    print_success "ragforge命令已安装到 /usr/local/bin/ragforge"
}

# 创建配置文件
create_config() {
    print_info "创建默认配置文件..."
    
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
  format: "table"  # table, json, yaml
  colors: true
  verbose: false

# 调试配置
debug:
  enabled: false
  level: "INFO"
EOF
        print_success "默认配置文件已创建: config.yaml"
    else
        print_warning "配置文件已存在: config.yaml"
    fi
}

# 验证安装
verify_installation() {
    print_info "验证安装..."
    
    if command -v ragforge &> /dev/null; then
        print_success "ragforge命令安装成功"
        
        # 测试命令
        print_info "测试ragforge命令..."
        ragforge version
        
        print_success "安装验证完成！"
    else
        print_error "ragforge命令安装失败"
        exit 1
    fi
}

# 显示使用说明
show_usage() {
    print_info "安装完成！"
    echo
    echo "使用方法："
    echo "  ragforge --help                    # 显示帮助信息"
    echo "  ragforge user login               # 用户登录"
    echo "  ragforge user info                # 查看用户信息"
    echo "  ragforge datasets list            # 列出数据集"
    echo "  ragforge documents list <kb_id>   # 列出文档"
    echo "  ragforge debug check-connection   # 检查连接"
    echo
    echo "配置文件位置: $(pwd)/config.yaml"
    echo "请根据你的RAGForge服务器地址修改配置文件中的base_url"
}

# 主安装流程
main() {
    echo "=========================================="
    echo "    RAGForge Shell 安装脚本"
    echo "=========================================="
    echo
    
    check_python
    check_pip
    
    # 询问是否使用虚拟环境
    read -p "是否创建虚拟环境？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        create_venv
    else
        install_dependencies
    fi
    
    create_command
    create_config
    verify_installation
    show_usage
}

# 运行主函数
main "$@" 