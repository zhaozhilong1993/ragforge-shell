# RAGForge Shell 文件上传使用指南

## 概述

RAGForge Shell 提供了强大的文件上传功能，支持多种文件格式，可以轻松将文档上传到数据集中进行管理和检索。

## 快速开始

### 1. 基本文件上传

```bash
# 上传文件到指定数据集
uv run python main.py documents upload <dataset_id> --file <file_path>

# 示例
uv run python main.py documents upload 083591d662c911f08ba44a90b26523d1 --file my_document.pdf
```

### 2. 查看上传结果

```bash
# 查看数据集中的文档列表
uv run python main.py documents list <dataset_id>

# 查看文档详细信息
uv run python main.py documents show <dataset_id> <document_id>
```

### 3. 检索文档内容

```bash
# 在数据集中检索文档内容
uv run python main.py retrieval search "查询内容" <dataset_id>
```

## 支持的文件格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | `.pdf` | Adobe PDF文档 |
| Word | `.doc`, `.docx` | Microsoft Word文档 |
| 文本 | `.txt`, `.md` | 纯文本文件 |
| 其他 | 根据系统配置 | 支持更多格式 |

## 完整工作流程示例

### 步骤1: 检查系统状态
```bash
uv run python main.py system status
```

### 步骤2: 查看数据集列表
```bash
uv run python main.py datasets list
```

### 步骤3: 上传文件
```bash
uv run python main.py documents upload <dataset_id> --file <file_path>
```

### 步骤4: 验证上传结果
```bash
uv run python main.py documents list <dataset_id>
```

### 步骤5: 检索文档内容
```bash
uv run python main.py retrieval search "查询内容" <dataset_id>
```

## 自动化脚本

### 完整演示脚本
```bash
# 运行完整的文件上传演示
uv run python examples/file_upload_example.py
```

### 简单上传脚本
```bash
# 使用简单上传脚本
uv run python examples/simple_upload.py <dataset_id> <file_path>
```

## 使用示例

### 示例1: 上传PDF文档
```bash
# 上传PDF文件
uv run python main.py documents upload 083591d662c911f08ba44a90b26523d1 --file report.pdf

# 查看上传结果
uv run python main.py documents list 083591d662c911f08ba44a90b26523d1

# 检索PDF内容
uv run python main.py retrieval search "报告内容" 083591d662c911f08ba44a90b26523d1
```

### 示例2: 上传文本文件
```bash
# 上传文本文件
uv run python main.py documents upload 083591d662c911f08ba44a90b26523d1 --file notes.txt

# 查看文档详情
uv run python main.py documents list 083591d662c911f08ba44a90b26523d1 --format json
```

### 示例3: 批量上传
```bash
# 创建上传脚本
for file in *.pdf; do
    uv run python main.py documents upload 083591d662c911f08ba44a90b26523d1 --file "$file"
done
```

## 高级功能

### 1. 查看文档处理状态
```bash
# 查看文档的详细状态
uv run python main.py documents list <dataset_id> --format json
```

### 2. 查看文档块
```bash
# 查看文档的块信息
uv run python main.py documents chunks <dataset_id> <document_id>
```

### 3. 高级检索
```bash
# 使用高级检索选项
uv run python main.py retrieval search "查询内容" <dataset_id> \
  --top-k 10 \
  --similarity-threshold 0.8 \
  --highlight
```

## 注意事项

### 1. 文件大小限制
- 单个文件大小通常限制在几MB到几十MB
- 具体限制取决于系统配置

### 2. 文件编码
- 文本文件建议使用UTF-8编码
- 确保文件内容正确显示

### 3. 处理时间
- 文档处理可能需要一些时间
- 大型PDF文件处理时间较长
- 可以使用文档列表查看处理状态

### 4. 认证要求
- 需要有效的API token
- 确保配置文件中的认证信息正确

## 故障排除

### 常见问题

1. **上传失败**
   ```bash
   # 检查系统状态
   uv run python main.py system status
   
   # 检查认证状态
   uv run python main.py user status
   ```

2. **文档处理失败**
   ```bash
   # 查看文档状态
   uv run python main.py documents list <dataset_id> --format json
   ```

3. **检索无结果**
   ```bash
   # 检查文档是否已处理完成
   uv run python main.py documents list <dataset_id>
   
   # 尝试不同的查询词
   uv run python main.py retrieval search "其他关键词" <dataset_id>
   ```

### 调试命令

```bash
# 检查API连接
uv run python main.py debug check-connection

# 测试API调用
uv run python main.py debug test-api /api/v1/datasets/<dataset_id>/documents

# 查看配置信息
uv run python main.py config-show
```

## 最佳实践

1. **文件准备**
   - 确保文件格式正确
   - 检查文件编码
   - 验证文件完整性

2. **上传流程**
   - 先检查系统状态
   - 确认数据集存在
   - 验证上传结果

3. **内容检索**
   - 使用相关的关键词
   - 尝试不同的查询方式
   - 检查文档处理状态

4. **错误处理**
   - 查看详细的错误信息
   - 使用调试工具排查问题
   - 检查网络连接和认证状态

## 总结

RAGForge Shell 的文件上传功能提供了：

- ✅ **简单易用**: 一条命令完成文件上传
- ✅ **多格式支持**: PDF、Word、文本等多种格式
- ✅ **完整流程**: 从上传到检索的完整工作流
- ✅ **自动化脚本**: 提供演示和批量上传脚本
- ✅ **详细文档**: 完整的使用指南和示例
- ✅ **错误处理**: 完善的错误处理和调试工具

通过这个功能，用户可以轻松地将各种文档上传到RAGForge系统中，进行统一管理和智能检索。 