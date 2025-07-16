# RAGForge API 脚本工具 - 使用说明

## 概述

这个脚本工具封装了RAGForge API的所有功能，提供了简洁易用的命令行接口。主要功能包括：

- **数据集管理**: 创建、查看、更新、删除数据集
- **文档管理**: 在数据集中管理文档
- **文档块管理**: 管理文档的块和关键词
- **检索功能**: 基于语义的文档检索

## 快速开始

### 1. 环境准备

```bash
# 激活虚拟环境
source venv/bin/activate

# 检查API连接
python main.py api-list
```

### 2. 基本工作流程

#### 创建数据集
```bash
# 创建新数据集
python main.py datasets create "我的知识库" --description "包含各种技术文档的数据集"
```

#### 添加文档
```bash
# 在数据集中创建文档
python main.py documents create <dataset_id> "机器学习基础" --content "机器学习是人工智能的一个分支..."
```

#### 添加文档块
```bash
# 向文档添加块
python main.py chunks add <dataset_id> <document_id> "机器学习通过算法从数据中学习模式" --keywords "机器学习,算法,数据"
```

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
python main.py datasets list

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
python main.py documents list <dataset_id>

# 查看文档详情
python main.py documents show <dataset_id> <document_id>

# 创建文档
python main.py documents create <dataset_id> "文档名称" --content "文档内容"

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

# 3. 添加文档块
python main.py chunks add <dataset_id> <document_id> "Python的语法简洁明了，适合初学者学习" --keywords "Python,语法,初学者"

# 4. 检索内容
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

### 示例3: 文档内容管理

```bash
# 查看文档的所有块
python main.py documents chunks <dataset_id> <document_id>

# 更新特定块
python main.py chunks update <dataset_id> <document_id> <chunk_id> \
  --content "更新后的内容" \
  --keywords "新关键词1,新关键词2"
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
   # 在config.yaml中添加认证头
   api:
     headers:
       Authorization: "Bearer your_token_here"
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
        '--description', description, '--format', 'json'
    ], capture_output=True, text=True)
    return json.loads(result.stdout)

def search_content(question, dataset_id):
    result = subprocess.run([
        'python', 'main.py', 'retrieval', 'search', question, dataset_id,
        '--format', 'json'
    ], capture_output=True, text=True)
    return json.loads(result.stdout)
```

## 更多资源

- 查看 `README.md` 获取项目概述
- 查看 `QUICKSTART.md` 获取快速开始指南
- 运行 `python examples.py` 查看示例代码
- 使用 `python main.py --help` 查看所有可用命令 