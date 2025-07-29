# RAGForge Shell 安装指南

RAGForge Shell 是一个命令行工具，提供了简洁易用的 RAGForge API 接口。

## 系统要求

- Python 3.7+
- pip3
- Linux/macOS/Windows (WSL)

## 安装方法

### 方法一：交互式安装（推荐）

```bash
# 下载并运行安装脚本
curl -fsSL https://raw.githubusercontent.com/your-repo/ragforge/main/ragforge-shell/install.sh | bash

# 或者直接运行
./install.sh
```

### 方法二：快速安装（无交互）

```bash
# 下载并运行快速安装脚本
curl -fsSL https://raw.githubusercontent.com/your-repo/ragforge/main/ragforge-shell/quick_install.sh | bash

# 或者直接运行
./quick_install.sh
```

### 方法三：手动安装

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/ragforge.git
cd ragforge/ragforge-shell

# 2. 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 创建ragforge命令
sudo ln -s $(pwd)/main.py /usr/local/bin/ragforge
```

## 验证安装

安装完成后，运行以下命令验证：

```bash
# 检查版本
ragforge version

# 查看帮助
ragforge --help

# 检查连接
ragforge debug check-connection
```

## 配置

安装完成后，需要配置 `config.yaml` 文件：

```yaml
# RAGForge API 配置
api:
  base_url: "http://localhost:9380"  # 修改为你的RAGForge服务器地址
  timeout: 30
  retries: 3

# 认证配置
auth:
  username: "your_username"
  password: "your_password"
  api_key: "your_api_key"
```

## 使用方法

### 基本命令

```bash
# 用户管理
ragforge user login                    # 用户登录
ragforge user info                     # 查看用户信息
ragforge user register                 # 用户注册

# 数据集管理
ragforge datasets list                 # 列出数据集
ragforge datasets create               # 创建数据集
ragforge datasets delete <dataset_id>  # 删除数据集

# 文档管理
ragforge documents list <kb_id>        # 列出文档
ragforge documents upload <kb_id>      # 上传文档
ragforge documents delete <doc_id>     # 删除文档

# 检索
ragforge retrieval search "查询内容" <kb_id>  # 搜索文档

# 调试
ragforge debug check-connection        # 检查连接
ragforge debug api-list                # 列出API端点
```

### 高级用法

```bash
# 使用不同的输出格式
ragforge datasets list --format json
ragforge datasets list --format yaml

# 启用调试模式
ragforge --debug datasets list

# 使用自定义配置文件
ragforge --config my_config.yaml datasets list
```

## 卸载

如果需要卸载 RAGForge Shell：

```bash
# 运行卸载脚本
./uninstall.sh

# 或者手动卸载
sudo rm -f /usr/local/bin/ragforge
rm -rf .venv
```

## 故障排除

### 常见问题

1. **命令未找到**
   ```bash
   # 检查命令是否安装
   which ragforge
   
   # 重新安装
   ./install.sh
   ```

2. **连接失败**
   ```bash
   # 检查配置文件
   cat config.yaml
   
   # 测试连接
   ragforge debug check-connection
   ```

3. **权限问题**
   ```bash
   # 检查权限
   ls -la /usr/local/bin/ragforge
   
   # 修复权限
   sudo chmod +x /usr/local/bin/ragforge
   ```

### 日志和调试

```bash
# 启用详细输出
ragforge --debug --verbose datasets list

# 查看Python错误
ragforge --debug datasets list 2>&1 | grep -i error
```

## 开发

### 本地开发

```bash
# 激活虚拟环境
source .venv/bin/activate

# 直接运行
python main.py --help

# 运行测试
python -m pytest tests/
```

### 贡献

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。

## 支持

如果遇到问题，请：

1. 查看 [FAQ](https://github.com/your-repo/ragforge/wiki/FAQ)
2. 提交 [Issue](https://github.com/your-repo/ragforge/issues)
3. 加入 [Discord](https://discord.gg/ragforge) 