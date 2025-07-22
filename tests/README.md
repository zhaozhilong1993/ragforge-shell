# 压力测试脚本

本目录包含用于测试RAGForge系统稳定性的压力测试脚本。

## 脚本说明

### 1. 快速测试脚本 (`quick_test.sh`)
- **用途**: 验证压力测试功能是否正常工作
- **文档数量**: 100个文档
- **批次大小**: 10个文档/批次
- **预计时间**: 5-10分钟
- **数据集**: `quick_test_dataset`

### 2. 压力测试脚本 (`stress_test.sh`)
- **用途**: 完整的压力测试，测试系统在大量文档下的稳定性
- **文档数量**: 100,000个文档
- **批次大小**: 100个文档/批次
- **预计时间**: 2-4小时（取决于系统性能）
- **数据集**: `stress_test_dataset`

## 使用方法

### 前置条件
1. 确保已安装Python和uv
2. 确保已登录RAGForge系统
3. 确保有足够的磁盘空间（建议至少1GB）

### 快速测试（推荐先运行）
```bash
# 先登录系统
uv run python main.py user login <email> <password>

# 运行快速测试
./tests/quick_test.sh
```

### 完整压力测试
```bash
# 确保快速测试通过后，运行完整压力测试
./tests/stress_test.sh
```

## 脚本功能

### 自动检查
- ✅ 依赖检查（Python、uv）
- ✅ 认证状态检查
- ✅ 数据集管理（创建/删除）

### 文档生成
- ✅ 自动生成测试文档
- ✅ 使用模板系统
- ✅ 包含时间戳和唯一ID

### 批量上传
- ✅ 分批处理，避免系统过载
- ✅ 实时进度显示
- ✅ 错误统计和报告

### 结果验证
- ✅ 上传成功率统计
- ✅ 系统性能指标
- ✅ 详细日志记录

## 输出文件

### 日志文件
- `tests/stress_test.log` - 压力测试日志
- `tests/quick_test.log` - 快速测试日志

### 临时文件
- `tests/temp_docs/` - 压力测试临时文档
- `tests/temp_docs_quick/` - 快速测试临时文档

## 监控指标

### 性能指标
- **上传速率**: 文档/秒
- **成功率**: 成功上传的文档百分比
- **总耗时**: 完整测试所需时间
- **错误率**: 失败上传的文档数量

### 系统指标
- **CPU使用率**: 系统CPU负载
- **内存使用**: 系统内存使用情况
- **磁盘空间**: 存储空间使用情况
- **网络延迟**: API响应时间

## 故障排除

### 常见问题

1. **认证失败**
   ```bash
   # 重新登录
   uv run python main.py user login <email> <password>
   ```

2. **数据集创建失败**
   ```bash
   # 检查现有数据集
   uv run python main.py datasets list
   
   # 删除冲突的数据集
   uv run python main.py datasets delete <dataset_name>
   ```

3. **文档上传失败**
   - 检查网络连接
   - 检查磁盘空间
   - 查看详细日志文件

4. **脚本权限问题**
   ```bash
   # 添加执行权限
   chmod +x tests/*.sh
   ```

### 日志分析
```bash
# 查看测试日志
tail -f tests/stress_test.log

# 查看错误信息
grep "ERROR" tests/stress_test.log

# 查看成功率
grep "成功率" tests/stress_test.log
```

## 自定义配置

### 修改文档数量
编辑脚本中的 `TOTAL_DOCUMENTS` 变量：
```bash
# 压力测试脚本
TOTAL_DOCUMENTS=100000

# 快速测试脚本
TOTAL_DOCUMENTS=100
```

### 修改批次大小
编辑脚本中的 `BATCH_SIZE` 变量：
```bash
# 压力测试脚本
BATCH_SIZE=100

# 快速测试脚本
BATCH_SIZE=10
```

### 修改数据集名称
编辑脚本中的 `DATASET_NAME` 变量：
```bash
DATASET_NAME="my_stress_test_dataset"
```

## 注意事项

1. **系统资源**: 压力测试会消耗大量系统资源，建议在非生产环境运行
2. **网络稳定性**: 确保网络连接稳定，避免上传中断
3. **磁盘空间**: 确保有足够的磁盘空间存储测试文档
4. **时间安排**: 完整压力测试需要较长时间，建议在空闲时间运行
5. **监控系统**: 运行测试时建议监控系统资源使用情况

## 测试报告

测试完成后，脚本会生成详细的测试报告，包括：
- 总上传文档数量
- 成功/失败统计
- 平均上传速率
- 系统性能指标
- 错误日志和故障排除建议 