# RAGForge API 脚本工具 - 快速开始指南

## 安装

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置API地址：
编辑 `config.yaml` 文件，设置正确的API基础URL：
```yaml
api:
  base_url: "http://localhost:9380"  # 修改为你的API地址
```

## 基本使用

### 1. 查看帮助
```bash
python main.py --help
```

### 2. 数据集管理
```bash
# 列出所有数据集
python main.py datasets list

# 显示数据集详情
python main.py datasets show <dataset_id>

# 创建新数据集
python main.py datasets create "我的数据集" --description "数据集描述"

# 删除数据集
python main.py datasets delete <dataset_id>

# 更新数据集
python main.py datasets update <dataset_id> "新名称" --description "新描述"
```

### 3. 文档管理
```bash
# 列出数据集中的所有文档
python main.py documents list <dataset_id>

# 显示文档详情
python main.py documents show <dataset_id> <document_id>

# 创建新文档
python main.py documents create <dataset_id> "文档名称" --content "文档内容"

# 删除文档
python main.py documents delete <dataset_id> <document_id>

# 更新文档
python main.py documents update <dataset_id> <document_id> "新名称" --content "新内容"

# 查看文档的块
python main.py documents chunks <dataset_id> <document_id>
```

### 4. 文档块管理
```bash
# 显示块详情
python main.py chunks show <dataset_id> <document_id> <chunk_id>

# 添加新块
python main.py chunks add <dataset_id> <document_id> "块内容" --keywords "关键词1,关键词2"

# 更新块
python main.py chunks update <dataset_id> <document_id> <chunk_id> --content "新内容" --keywords "新关键词"

# 删除块
python main.py chunks delete <dataset_id> <document_id> <chunk_id>
```

### 5. 检索功能
```bash
# 跨数据集检索
python main.py retrieval search "查询内容" <dataset_id1> <dataset_id2>

# 单数据集检索
python main.py retrieval search-single-dataset "查询内容" <dataset_id>

# 单文档检索
python main.py retrieval search-single-document "查询内容" <dataset_id> <document_id>

# 高级检索选项
python main.py retrieval search "查询内容" <dataset_id> --top-k 5 --similarity-threshold 0.8 --highlight
```

### 6. 通用API调用
```bash
# 列出所有API端点
python main.py api-list

# 直接调用API
python main.py api-call /api/v1/datasets --method GET

# 显示当前配置
python main.py config-show
```

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

## 示例脚本

运行示例脚本查看各种操作：
```bash
python examples.py
```

## 扩展新命令

1. 在 `commands/` 目录下创建新的命令文件
2. 使用Click装饰器定义命令
3. 在 `main.py` 中注册新命令

示例：
```python
# commands/my_service.py
import click
from api_client import APIClient
from utils.output import OutputFormatter

@click.group()
def my_service():
    """我的服务命令"""
    pass

@my_service.command()
def list():
    """列出资源"""
    client = APIClient()
    response = client.get('/api/v1/my-resources')
    # 处理响应...
```

然后在 `main.py` 中注册：
```python
from commands.my_service import my_service
cli.add_command(my_service, name='my-service')
```

## 故障排除

1. **连接错误**：检查 `config.yaml` 中的API地址是否正确
2. **认证错误**：确认API是否需要认证，在配置中添加认证头
3. **权限错误**：确认API端点权限设置

## 更多信息

- 查看 `README.md` 获取详细文档
- 运行 `python main.py --help` 查看所有可用命令
- 查看 `examples.py` 了解具体使用示例 