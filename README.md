# RAGForge API 脚本工具

这是一个用于封装RAGForge API调用的Python脚本工程，提供了简洁易用的命令行接口。

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```bash
# 列出所有可用的命令
python main.py --help

# 数据集管理
python main.py datasets list
python main.py datasets create "我的数据集"

# 文档管理
python main.py documents list <dataset_id>
python main.py documents create <dataset_id> "文档名称"

# 检索功能
python main.py retrieval search "查询内容" <dataset_id>
```

### 配置

在 `config.yaml` 中配置API基础URL和认证信息：

```yaml
api:
  base_url: "http://localhost:9380"
  timeout: 30
  headers:
    Content-Type: "application/json"
```

## 项目结构

- `main.py`: 主入口脚本
- `api_client.py`: API客户端封装
- `commands/`: 各种API命令模块
  - `datasets.py`: 数据集管理
  - `documents.py`: 文档管理
  - `chunks.py`: 文档块管理
  - `retrieval.py`: 检索功能
- `config.yaml`: 配置文件
- `utils/`: 工具函数

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

## 添加新命令

1. 在 `commands/` 目录下创建新的命令模块
2. 在 `main.py` 中注册新命令
3. 更新文档 