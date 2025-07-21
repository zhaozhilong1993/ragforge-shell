# RAGForge Shell 命令文档

## 概述

RAGForge Shell 是一个命令行工具，提供了对 RAGForge API 的完整访问。支持用户管理、系统管理、数据集管理、文档管理、检索等功能。

## 基本用法

```bash
# 使用 uv 运行（推荐）
uv run python main.py [命令] [子命令] [参数]

# 或者激活环境后运行
uv shell
python main.py [命令] [子命令] [参数]
```

## 命令分类

### 1. 用户管理 (user)

#### 用户认证
```bash
# 用户登录
python main.py user login <email> <password>

# 用户登出
python main.py user logout

# 用户注册
python main.py user register <email> <password> <nickname>

# 检查认证状态
python main.py user status
```

#### 用户信息
```bash
# 获取当前用户信息
python main.py user info

# 获取租户信息
python main.py user tenant-info

# 更新用户设置
python main.py user setting <email> <nickname>
```

#### 密码管理
```bash
# 修改密码（需要先登录）
python main.py user change-password <old_password> <new_password>

# 重置密码（忘记密码时使用）
python main.py user reset-password <email> <new_password>
```

#### 第三方登录
```bash
# 飞书登录回调
python main.py user feishu-callback <code>

# GitHub登录回调
python main.py user github-callback <code>
```

#### 租户管理
```bash
# 设置租户信息
python main.py user set-tenant-info <tenant_info_json>
```

### 2. 系统管理 (system)

#### 系统信息
```bash
# 获取系统状态
python main.py system status

# 获取系统版本
python main.py system version

# 获取系统配置
python main.py system config

# 获取接口配置
python main.py system interface-config
```

#### 令牌管理
```bash
# 生成新的API令牌
python main.py system new-token

# 获取令牌信息
python main.py system token-info <token>

# 获取令牌列表
python main.py system token-list
```

#### 文件上传
```bash
# 上传接口文件
python main.py system upload-interface <file_path>
```

### 3. 数据集管理 (datasets)

#### 数据集操作
```bash
# 列出所有数据集
python main.py datasets list

# 显示数据集详情
python main.py datasets show <dataset_id>

# 创建数据集
python main.py datasets create <name> [--description <description>]

# 更新数据集
python main.py datasets update <dataset_id> <name> [--description <description>]

# 删除数据集
python main.py datasets delete <dataset_id>
```

### 4. 文档管理 (documents)

#### 文档操作
```bash
# 列出数据集中的文档
python main.py documents list <dataset_id>

# 显示文档详情
python main.py documents show <dataset_id> <document_id>

# 创建文档
python main.py documents create <dataset_id> <name> [--content <content>]

# 更新文档
python main.py documents update <dataset_id> <document_id> <name> [--content <content>]

# 删除文档
python main.py documents delete <dataset_id> <document_id>

# 上传文档文件
python main.py documents upload <dataset_id> --file <file_path>
```

#### 文档块管理
```bash
# 查看文档的块
python main.py documents chunks <dataset_id> <document_id>
```

### 5. 文档块管理 (chunks)

#### 块操作
```bash
# 列出数据集的所有块
python main.py chunks list <dataset_id>

# 显示块详情
python main.py chunks show <dataset_id> <chunk_id>

# 删除块
python main.py chunks delete <dataset_id> <chunk_id>
```

### 6. 检索功能 (retrieval)

#### 检索操作
```bash
# 多数据集检索
python main.py retrieval search <question> <dataset_id1> <dataset_id2>... [--top-k <number>]

# 单数据集检索
python main.py retrieval search-single-dataset <question> <dataset_id> [--top-k <number>]

# 单文档检索
python main.py retrieval search-single-document <question> <dataset_id> <document_id> [--top-k <number>]
```

#### 检索选项
- `--document-ids`: 指定文档ID列表（逗号分隔）
- `--top-k`: 返回的最大块数量（默认10）
- `--similarity-threshold`: 相似度阈值
- `--vector-similarity-weight`: 向量相似度权重
- `--highlight`: 是否高亮匹配内容

### 7. 调试功能 (debug)

#### 调试工具
```bash
# 测试API调用
python main.py debug test-api <endpoint> [--method <method>] [--data <json_data>]

# 检查连接状态
python main.py debug check-connection

# 原始API调用
python main.py debug raw-call <endpoint>
```

### 8. 通用功能

#### 配置和API
```bash
# 显示当前配置
python main.py config-show

# 列出所有API端点
python main.py api-list [--format <format>]

# 直接调用API
python main.py api-call <endpoint> [--method <method>] [--data <json_data>] [--format <format>]

# 显示版本信息
python main.py version
```

## 输出格式

所有命令都支持多种输出格式：

- `--format table`: 表格格式（默认）
- `--format json`: JSON格式
- `--format yaml`: YAML格式
- `--format simple`: 简单列表格式（部分命令支持）

## 配置文件

工具使用 `config.yaml` 配置文件，包含：

```yaml
api:
  api_token: your-api-token
  auth_token: your-auth-token
  base_url: http://localhost:9380
  headers:
    Accept: application/json
    Content-Type: application/json
  timeout: 30
logging:
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  level: INFO
output:
  format: table
  max_width: 120
```

## 示例用法

### 基本工作流程

1. **登录系统**
```bash
python main.py user login your-email@example.com your-password
```

2. **检查系统状态**
```bash
python main.py system status
```

3. **创建数据集**
```bash
python main.py datasets create "我的数据集" --description "用于测试的数据集"
```

4. **上传文档**
```bash
python main.py documents upload <dataset_id> --file /path/to/document.pdf
```

5. **检索文档**
```bash
python main.py retrieval search "你的问题" <dataset_id>
```

### 高级用法

**多数据集检索**
```bash
python main.py retrieval search "复杂查询问题" dataset1 dataset2 dataset3 --top-k 20 --highlight
```

**获取系统信息**
```bash
python main.py system status --format json
python main.py system version --format yaml
```

**调试API调用**
```bash
python main.py debug test-api /api/v1/datasets --method GET
```

## 错误处理

工具提供了完善的错误处理机制：

- 网络连接错误
- API认证错误
- 数据格式错误
- 文件上传错误

所有错误都会显示详细的错误信息，帮助用户快速定位问题。

## 注意事项

1. 首次使用前需要配置 `config.yaml` 文件
2. 使用 `uv run` 确保在正确的环境中运行
3. 某些命令需要先登录才能使用
4. 文件上传功能支持多种格式（PDF、DOC、TXT等）
5. 检索功能支持多种参数调优 