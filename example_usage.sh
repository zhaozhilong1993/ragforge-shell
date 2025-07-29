#!/bin/bash

# RAGForge Shell 使用示例

echo "=========================================="
echo "    RAGForge Shell 使用示例"
echo "=========================================="
echo

# 检查ragforge命令是否安装
if ! command -v ragforge &> /dev/null; then
    echo "❌ ragforge命令未安装，请先运行 ./quick_install.sh"
    exit 1
fi

echo "✅ ragforge命令已安装"
echo

# 显示版本信息
echo "📋 版本信息："
ragforge version
echo

# 显示帮助信息
echo "📖 帮助信息："
ragforge --help
echo

# 显示用户命令帮助
echo "👤 用户管理命令："
ragforge user --help
echo

# 显示数据集命令帮助
echo "📊 数据集管理命令："
ragforge datasets --help
echo

# 显示文档命令帮助
echo "📄 文档管理命令："
ragforge documents --help
echo

# 显示调试命令帮助
echo "🔧 调试命令："
ragforge debug --help
echo

echo "=========================================="
echo "    使用示例"
echo "=========================================="
echo

echo "1. 用户登录："
echo "   ragforge user login"
echo

echo "2. 查看用户信息："
echo "   ragforge user info"
echo

echo "3. 列出数据集："
echo "   ragforge datasets list"
echo

echo "4. 查看文档："
echo "   ragforge documents list <kb_id>"
echo

echo "5. 搜索文档："
echo "   ragforge retrieval search '查询内容' <kb_id>"
echo

echo "6. 检查连接："
echo "   ragforge debug check-connection"
echo

echo "7. 查看API列表："
echo "   ragforge api-list"
echo

echo "8. 直接调用API："
echo "   ragforge api-call /v1/user/info"
echo

echo "注意：使用前请确保："
echo "1. RAGForge服务器正在运行"
echo "2. 配置文件 config.yaml 中的 base_url 正确"
echo "3. 已登录用户（ragforge user login）" 