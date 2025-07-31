# 数据集管理命令使用说明

## 新增功能

### 1. 修复embedding模型
```bash
python main.py datasets fix-embedding-model <dataset_id>
```
- **功能**: 自动将数据集的embedding模型修复为默认的embedding模型
- **使用场景**: 当数据集使用错误的embedding模型导致任务处理失败时
- **示例**: `python main.py datasets fix-embedding-model 78a084ae6c5011f090704a90b26523d1`

### 2. 设置embedding模型
```bash
python main.py datasets set-embedding-model <dataset_id> <embedding_model> [--force]
```
- **功能**: 手动设置数据集的embedding模型
- **参数**:
  - `dataset_id`: 数据集ID
  - `embedding_model`: 新的embedding模型名称
  - `--force`: 强制更新，不提示确认
- **示例**: `python main.py datasets set-embedding-model 78a084ae6c5011f090704a90b26523d1 bge-m3___OpenAI-API --force`

### 3. 删除数据集
```bash
python main.py datasets delete <dataset_id> [--force]
```
- **功能**: 删除数据集，支持多种删除方法
- **参数**:
  - `dataset_id`: 数据集ID
  - `--force`: 强制删除，不提示确认
- **特性**:
  - 删除前会显示数据集名称
  - 支持多种删除方法（DELETE、POST、PUT标记删除）
  - 提供详细的错误信息和操作建议
  - 自动验证删除结果

### 4. 彻底删除数据集
```bash
python main.py datasets purge <dataset_id> [--force]
```
- **功能**: 彻底删除数据集，尝试所有可能的删除方法
- **参数**:
  - `dataset_id`: 数据集ID
  - `--force`: 强制删除，不提示确认
- **特性**:
  - 尝试多种删除方法
  - 提供详细的操作建议
  - 如果API删除失败，会建议通过Web界面删除

## 使用示例

### 修复embedding模型问题
```bash
# 1. 查看当前数据集列表
python main.py datasets list

# 2. 修复embedding模型
python main.py datasets fix-embedding-model 78a084ae6c5011f090704a90b26523d1

# 3. 验证修复结果
python main.py datasets list --format json
```

### 手动设置embedding模型
```bash
# 设置特定的embedding模型
python main.py datasets set-embedding-model 78a084ae6c5011f090704a90b26523d1 bge-m3___OpenAI-API --force
```

### 删除数据集
```bash
# 删除数据集（会提示确认）
python main.py datasets delete 78a084ae6c5011f090704a90b26523d1

# 强制删除数据集（不提示确认）
python main.py datasets delete 78a084ae6c5011f090704a90b26523d1 --force
```

### 彻底删除数据集
```bash
# 彻底删除数据集（会提示确认）
python main.py datasets purge 78a084ae6c5011f090704a90b26523d1

# 强制彻底删除数据集（不提示确认）
python main.py datasets purge 78a084ae6c5011f090704a90b26523d1 --force
```

## 常见问题解决

### 问题1: "Model(embed) not authorized" 错误
**原因**: 数据集使用了不存在的embedding模型
**解决方案**: 
```bash
python main.py datasets fix-embedding-model <dataset_id>
```

### 问题2: 删除数据集失败
**原因**: API不支持直接删除
**解决方案**: 
```bash
# 尝试使用脚本的删除功能
python main.py datasets delete <dataset_id> --force

# 如果仍然失败，使用彻底删除功能
python main.py datasets purge <dataset_id> --force

# 如果API删除都失败，通过Web界面手动删除
```

### 问题3: 更新embedding模型失败
**原因**: API不支持直接更新embedding模型
**解决方案**:
```bash
# 1. 删除现有数据集
python main.py datasets delete <dataset_id> --force

# 2. 重新创建数据集（会自动使用默认embedding模型）
python main.py datasets create "新数据集名称"
```

### 问题4: 数据集删除后仍然存在
**原因**: API只支持标记删除，不真正删除数据
**解决方案**:
```bash
# 1. 尝试彻底删除
python main.py datasets purge <dataset_id> --force

# 2. 如果仍然存在，通过Web界面手动删除
# 3. 或者联系管理员删除
```

## 删除功能对比

| 命令 | 功能 | 特点 | 适用场景 |
|------|------|------|----------|
| `delete` | 标准删除 | 尝试多种方法，验证结果 | 一般删除操作 |
| `purge` | 彻底删除 | 尝试所有方法，提供建议 | 需要彻底删除时 |

## 技术说明

### API调用方法
脚本会尝试多种API调用方法：
1. **直接DELETE请求**: 删除数据集
2. **POST请求**: 通过特殊端点删除
3. **PUT请求**: 标记删除状态
4. **验证删除**: 检查数据集是否真的被删除

### 错误处理
- 提供详细的错误信息
- 自动尝试多种解决方案
- 给出操作建议
- 区分不同类型的删除结果

### 认证支持
- 支持Bearer token认证
- 自动处理认证头
- 配置文件保存认证信息

### 状态反馈
- ✅ 成功删除
- ⚠️ 标记删除（可能仍存在）
- ❌ 删除失败
- ℹ️ 操作建议 