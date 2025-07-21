# RAGForge Shell 文档解析使用指南

## 概述

RAGForge Shell 提供了强大的文档解析功能，可以将上传的文档（PDF、DOC、TXT等）解析成可检索的文本块。

## 文档解析状态

文档有以下几种解析状态：

- **UNSTART**: 未开始解析
- **RUNNING**: 正在解析中
- **FINISHED**: 解析完成
- **FAILED**: 解析失败

## 基本命令

### 1. 查看文档解析状态

```bash
# 查看单个文档的解析状态
uv run python main.py documents status <dataset_id> <document_id>

# 示例
uv run python main.py documents status 083591d662c911f08ba44a90b26523d1 d91fdb98663f11f0a6b6be2f4eecc70e
```

### 2. 启动单个文档解析

```bash
# 启动单个文档的解析
uv run python main.py documents parse <dataset_id> <document_id>

# 示例
uv run python main.py documents parse 083591d662c911f08ba44a90b26523d1 d91fdb98663f11f0a6b6be2f4eecc70e
```

### 3. 批量启动文档解析

```bash
# 批量启动所有未解析文档的解析
uv run python main.py documents parse-all <dataset_id>

# 示例
uv run python main.py documents parse-all 083591d662c911f08ba44a90b26523d1
```

### 4. 查看所有文档状态

```bash
# 查看数据集中所有文档的状态
uv run python main.py documents list <dataset_id> --format json | jq '.data.docs[] | {id, name, run, progress, progress_msg}'

# 示例
uv run python main.py documents list 083591d662c911f08ba44a90b26523d1 --format json | jq '.data.docs[] | {id, name, run, progress, progress_msg}'
```

## 完整工作流程

### 步骤1: 上传文档
```bash
# 上传文档到数据集
uv run python main.py documents upload <dataset_id> --file <file_path>
```

### 步骤2: 查看文档状态
```bash
# 查看文档是否已上传
uv run python main.py documents list <dataset_id>
```

### 步骤3: 启动解析
```bash
# 启动文档解析
uv run python main.py documents parse <dataset_id> <document_id>
```

### 步骤4: 监控解析进度
```bash
# 查看解析状态
uv run python main.py documents status <dataset_id> <document_id>
```

### 步骤5: 检索文档内容
```bash
# 解析完成后，可以检索文档内容
uv run python main.py retrieval search "查询内容" <dataset_id>
```

## 使用示例

### 示例1: 解析单个文档

```bash
# 1. 上传文档
uv run python main.py documents upload 083591d662c911f08ba44a90b26523d1 --file my_document.pdf

# 2. 获取文档ID
uv run python main.py documents list 083591d662c911f08ba44a90b26523d1 --format json | jq '.data.docs[0].id'

# 3. 启动解析
uv run python main.py documents parse 083591d662c911f08ba44a90b26523d1 <document_id>

# 4. 监控状态
uv run python main.py documents status 083591d662c911f08ba44a90b26523d1 <document_id>
```

### 示例2: 批量解析所有文档

```bash
# 1. 查看所有文档状态
uv run python main.py documents list 083591d662c911f08ba44a90b26523d1

# 2. 批量启动解析
uv run python main.py documents parse-all 083591d662c911f08ba44a90b26523d1

# 3. 等待解析完成
sleep 30

# 4. 检查解析结果
uv run python main.py documents list 083591d662c911f08ba44a90b26523d1 --format json | jq '.data.docs[] | {name, run, progress, chunk_count}'
```

### 示例3: 自动化解析脚本

```bash
#!/bin/bash

DATASET_ID="083591d662c911f08ba44a90b26523d1"

# 1. 上传文档
echo "上传文档..."
uv run python main.py documents upload $DATASET_ID --file document.pdf

# 2. 获取最新文档ID
DOC_ID=$(uv run python main.py documents list $DATASET_ID --format json | jq -r '.data.docs[0].id')

# 3. 启动解析
echo "启动解析..."
uv run python main.py documents parse $DATASET_ID $DOC_ID

# 4. 监控解析进度
echo "监控解析进度..."
while true; do
    STATUS=$(uv run python main.py documents status $DATASET_ID $DOC_ID --format json | jq -r '.run')
    PROGRESS=$(uv run python main.py documents status $DATASET_ID $DOC_ID --format json | jq -r '.progress')
    
    echo "状态: $STATUS, 进度: $PROGRESS"
    
    if [ "$STATUS" = "FINISHED" ]; then
        echo "解析完成！"
        break
    elif [ "$STATUS" = "FAILED" ]; then
        echo "解析失败！"
        break
    fi
    
    sleep 10
done

# 5. 测试检索
echo "测试检索..."
uv run python main.py retrieval search "文档内容" $DATASET_ID
```

## 解析状态说明

### 进度字段
- **progress**: 解析进度（0-1之间的小数）
- **progress_msg**: 进度消息
- **chunk_count**: 已生成的块数量
- **token_count**: 已处理的token数量

### 状态字段
- **run**: 解析运行状态
- **status**: 文档状态（1表示正常）

## 注意事项

### 1. 解析时间
- 文档解析是异步进行的
- 解析时间取决于文档大小和复杂度
- 大型PDF文件可能需要较长时间

### 2. 解析队列
- 系统有解析队列，文档会按顺序处理
- 可以同时启动多个文档的解析

### 3. 错误处理
- 如果解析失败，可以重新启动解析
- 检查文档格式是否支持

### 4. 资源限制
- 解析过程会消耗系统资源
- 建议分批处理大量文档

## 故障排除

### 常见问题

1. **解析不启动**
   ```bash
   # 检查API连接
   uv run python main.py debug check-connection
   
   # 检查认证状态
   uv run python main.py user status
   ```

2. **解析进度不更新**
   ```bash
   # 等待一段时间后再次检查
   sleep 30
   uv run python main.py documents status <dataset_id> <document_id>
   ```

3. **解析失败**
   ```bash
   # 查看详细错误信息
   uv run python main.py documents status <dataset_id> <document_id> --format json
   ```

### 调试命令

```bash
# 测试解析API
uv run python test_parse_api.py

# 查看系统状态
uv run python main.py system status

# 检查文档详情
uv run python main.py documents show <dataset_id> <document_id>
```

## 最佳实践

1. **文档准备**
   - 确保文档格式正确
   - 检查文档是否损坏
   - 使用标准编码格式

2. **解析策略**
   - 先解析小文档测试
   - 分批处理大量文档
   - 监控系统资源使用

3. **状态监控**
   - 定期检查解析状态
   - 记录解析时间和结果
   - 及时处理解析错误

4. **检索测试**
   - 解析完成后立即测试检索
   - 使用多种查询词测试
   - 验证检索结果质量

## 总结

RAGForge Shell 的文档解析功能提供了：

- ✅ **简单易用**: 一条命令启动解析
- ✅ **批量处理**: 支持批量启动解析
- ✅ **状态监控**: 实时查看解析进度
- ✅ **异步处理**: 不阻塞其他操作
- ✅ **错误处理**: 完善的错误处理机制
- ✅ **自动化脚本**: 支持自动化解析流程

通过这个功能，用户可以轻松地将各种文档解析成可检索的知识库内容。 