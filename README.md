# RAGForge API 脚本工具

这是一个用于封装RAGForge API调用的Python脚本工程，提供了简洁易用的命令行接口。

## 目录结构

```
ragforge-shell/
├── main.py                 # 主入口脚本
├── api_client.py           # API客户端封装
├── password_utils.py       # 密码加密工具
├── reset_password.py       # 密码重置工具
├── config.yaml             # 配置文件
├── requirements.txt        # 依赖包列表
├── commands/              # 命令模块目录
│   ├── datasets.py        # 数据集管理命令
│   ├── documents.py       # 文档管理命令
│   ├── chunks.py          # 文档块管理命令
│   ├── retrieval.py       # 检索功能命令
│   ├── user.py            # 用户管理命令
│   └── debug.py           # 调试命令
├── utils/                 # 工具函数目录
│   └── output.py          # 输出格式化工具
├── examples/              # 示例脚本目录
│   ├── example_usage.py   # 使用示例
│   ├── examples.py        # 更多示例
│   ├── quick_start.py     # 快速开始示例
│   └── try_login.py       # 登录示例
├── tests/                 # 测试脚本目录
│   ├── test_encryption.py # 加密测试
│   ├── test_auth_endpoints.py # 认证端点测试
│   ├── test_api.py        # API测试
│   └── check_api.py       # API连接检查
└── docs/                  # 文档目录
    ├── README.md          # 主文档
    ├── USAGE.md           # 详细使用说明
    ├── AUTH_README.md     # 认证说明
    └── QUICKSTART.md      # 快速开始指南
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 快速开始

### 1. 环境准备

```bash
# 检查API连接
python main.py debug check-connection

# 查看当前配置
python main.py config-show
```

### 2. 用户认证

```bash
# 用户注册
python main.py user register <username> <password>

# 用户登录
python main.py user login <username> <password>

# 查看用户状态
python main.py user status

# 查看用户信息
python main.py user info
```

### 3. 基本工作流程

#### 创建数据集
```bash
# 创建新数据集
python main.py datasets create "我的知识库" --description "包含各种技术文档的数据集"

# 查看数据集列表
python main.py datasets list --format simple
```

#### 添加文档
```bash
# 在数据集中创建文档
python main.py documents create <dataset_id> "机器学习基础" --content "机器学习是人工智能的一个分支..."

# 上传文件到数据集
python main.py documents upload <dataset_id> --file /path/to/document.pdf

# 查看数据集中的文档
python main.py documents list <dataset_id> --format simple
```

## 文件上传示例

### 完整工作流程演示

我们提供了一个完整的文件上传示例脚本，演示了从文件上传到检索的完整流程：

```bash
# 运行文件上传演示脚本
uv run python examples/file_upload_example.py
```

这个脚本会自动执行以下步骤：
1. 检查系统状态
2. 获取数据集列表
3. 创建测试文档
4. 上传文件到数据集
5. 查看文档列表
6. 查看文档详情
7. 尝试检索文档内容
8. 清理测试文件

### 手动文件上传流程

```bash
# 1. 查看数据集列表
uv run python main.py datasets list

# 2. 上传文件到指定数据集
uv run python main.py documents upload <dataset_id> --file <file_path>

# 3. 查看上传后的文档列表
uv run python main.py documents list <dataset_id>

# 4. 检索文档内容
uv run python main.py retrieval search "查询内容" <dataset_id>
```

### 支持的文件格式

- **PDF文件**: `.pdf`
- **Word文档**: `.doc`, `.docx`
- **文本文件**: `.txt`, `.md`
- **其他格式**: 根据系统配置支持更多格式

### 文件上传注意事项

1. **文件大小限制**: 根据系统配置，通常支持几MB到几十MB的文件
2. **文件编码**: 建议使用UTF-8编码的文本文件
3. **处理时间**: 文档处理可能需要一些时间，特别是大型PDF文件
4. **认证要求**: 需要有效的API token进行认证

#### 检索内容
```bash
# 在数据集中检索
python main.py retrieval search "什么是机器学习？" <dataset_id>

# 跨多个数据集检索
python main.py retrieval search "深度学习" <dataset_id1> <dataset_id2>
```

## 详细命令说明

### 数据集管理

```bash
# 列出所有数据集
python main.py datasets list --format simple

# 查看数据集详情
python main.py datasets show <dataset_id>

# 创建数据集
python main.py datasets create "数据集名称" --description "描述"

# 更新数据集
python main.py datasets update <dataset_id> "新名称" --description "新描述"

# 删除数据集
python main.py datasets delete <dataset_id>
```

### 文档管理

```bash
# 列出数据集中的所有文档
python main.py documents list <dataset_id> --format simple

# 查看文档详情
python main.py documents show <dataset_id> <document_id>

# 创建文档
python main.py documents create <dataset_id> "文档名称" --content "文档内容"

# 上传文件到数据集
python main.py documents upload <dataset_id> --file <file_path>

# 启动文档解析
python main.py documents parse <dataset_id> <document_id>

# 查看文档解析状态
python main.py documents status <dataset_id> <document_id>

# 批量启动文档解析
python main.py documents parse-all <dataset_id>

# 更新文档
python main.py documents update <dataset_id> <document_id> "新名称" --content "新内容"

# 删除文档
python main.py documents delete <dataset_id> <document_id>

# 查看文档的块
python main.py documents chunks <dataset_id> <document_id>
```

### 文档块管理

```bash
# 查看块详情
python main.py chunks show <dataset_id> <document_id> <chunk_id>

# 添加新块
python main.py chunks add <dataset_id> <document_id> "块内容" --keywords "关键词1,关键词2"

# 更新块
python main.py chunks update <dataset_id> <document_id> <chunk_id> --content "新内容" --keywords "新关键词"

# 删除块
python main.py chunks delete <dataset_id> <document_id> <chunk_id>
```

### 检索功能

```bash
# 基本检索
python main.py retrieval search "查询内容" <dataset_id>

# 跨数据集检索
python main.py retrieval search "查询内容" <dataset_id1> <dataset_id2>

# 单数据集检索
python main.py retrieval search-single-dataset "查询内容" <dataset_id>

# 单文档检索
python main.py retrieval search-single-document "查询内容" <dataset_id> <document_id>

# 高级检索选项
python main.py retrieval search "查询内容" <dataset_id> \
  --top-k 5 \
  --similarity-threshold 0.8 \
  --vector-similarity-weight 0.7 \
  --highlight
```

### 检索参数说明

- `--top-k`: 返回的最大块数量（默认10）
- `--similarity-threshold`: 相似度阈值（0-1之间）
- `--vector-similarity-weight`: 向量相似度权重
- `--highlight`: 是否高亮匹配内容
- `--document-ids`: 限制检索的文档ID列表

## 输出格式

所有命令都支持多种输出格式：

```bash
# 表格格式（默认）
python main.py datasets list

# 简洁列表格式
python main.py datasets list --format simple

# JSON格式
python main.py datasets list --format json

# YAML格式
python main.py datasets list --format yaml
```

## 实用示例

### 示例1: 创建技术文档知识库

```bash
# 1. 创建数据集
python main.py datasets create "技术文档库" --description "包含各种技术文档和教程"

# 2. 添加文档
python main.py documents create <dataset_id> "Python基础教程" --content "Python是一种高级编程语言..."

# 3. 检索内容
python main.py retrieval search "Python有什么特点？" <dataset_id>
```

### 示例2: 多数据集检索

```bash
# 在多个数据集中检索
python main.py retrieval search "机器学习算法" \
  dataset_tech \
  dataset_research \
  --top-k 10 \
  --similarity-threshold 0.6
```

## 测试和示例脚本

### 测试脚本 (tests/)

```bash
# 测试加密功能
python tests/test_encryption.py

# 测试认证端点
python tests/test_auth_endpoints.py

# 测试API连接
python tests/test_api.py

# 检查API连接
python tests/check_api.py
```

### 示例脚本 (examples/)

```bash
# 查看使用示例
python examples/example_usage.py

# 查看更多示例
python examples/examples.py

# 快速开始示例
python examples/quick_start.py

# 登录示例
python examples/try_login.py
```

## 配置

在 `config.yaml` 中配置API基础URL和认证信息：

```yaml
api:
  base_url: "http://localhost:9380"
  timeout: 30
  headers:
    Content-Type: "application/json"
```

## 故障排除

### 常见问题

1. **连接错误**
   ```bash
   # 检查API地址配置
   python main.py config-show
   ```

2. **认证错误**
   ```bash
   # 重新登录
   python main.py user login <username> <password>
   ```

3. **参数错误**
   ```bash
   # 查看命令帮助
   python main.py <command> --help
   ```

### 调试模式

```bash
# 启用调试模式
python main.py --debug datasets list
```

## 高级用法

### 批量操作

```bash
# 批量创建文档块
for content in "内容1" "内容2" "内容3"; do
  python main.py chunks add <dataset_id> <document_id> "$content" --keywords "关键词"
done
```

### 脚本集成

```python
#!/usr/bin/env python3
import subprocess
import json

def create_dataset(name, description):
    result = subprocess.run([
        'python', 'main.py', 'datasets', 'create', name, 
        '--description', description
    ], capture_output=True, text=True)
    return result.returncode == 0
```

## 添加新命令

1. 在 `commands/` 目录下创建新的命令模块
2. 在 `main.py` 中注册新命令
3. 更新文档

## 主要功能

### 数据集管理
- 创建、查看、更新、删除数据集
- 列出所有数据集

### 文档管理
- 在数据集中创建、查看、更新、删除文档
- 列出数据集中的所有文档
- 查看文档的块信息

### 文档块管理
- 向文档添加新的块
- 更新文档块内容和关键词
- 删除文档块

### 检索功能
- 跨数据集检索
- 单数据集检索
- 单文档检索
- 支持相似度阈值和权重调整

### 用户管理
- 用户注册和登录
- 查看用户状态和信息
- 自动认证token管理 