# RAGForge 用户认证脚本使用指南

## 概述

这个目录包含了用于与RAGForge API交互的Shell脚本工具，特别是用户认证功能。

## 文件说明

### 核心文件
- `user_auth.py` - 用户认证主脚本（注册、登录、登出）
- `api_client.py` - API客户端封装类
- `test_auth_endpoints.py` - API端点测试脚本
- `config.yaml` - 配置文件

### 其他文件
- `try_login.py` - 尝试不同登录方式的脚本
- `check_api.py` - API连接检查脚本
- `reset_password.py` - 密码重置脚本

## 快速开始

### 1. 安装依赖

```bash
cd ragforge-shelll
pip install -r requirements.txt
```

### 2. 确保RAGForge服务器运行

确保RAGForge API服务器在 `http://localhost:9380` 运行。

### 3. 测试API连接

```bash
python test_auth_endpoints.py
```

### 4. 用户注册

```bash
python user_auth.py register
```

交互式输入：
- 邮箱地址
- 密码
- 确认密码
- 用户名（可选）

### 5. 用户登录

```bash
python user_auth.py login
```

交互式输入：
- 邮箱地址
- 密码

### 6. 用户登出

```bash
python user_auth.py logout
```

## API端点说明

### 用户认证端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/v1/user/register` | POST | 用户注册 |
| `/v1/user/login` | POST | 用户登录 |
| `/v1/user/logout` | POST | 用户登出 |
| `/v1/user/profile` | GET | 获取用户信息 |

### 系统端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/v1/system/version` | GET | 获取系统版本 |
| `/v1/system/config` | GET | 获取系统配置 |

## 请求格式

### 用户注册
```json
{
  "email": "user@example.com",
  "password": "password123",
  "username": "username"  // 可选
}
```

### 用户登录
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

## 响应格式

### 成功响应
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "username": "username",
    "email": "user@example.com"
  }
}
```

### 错误响应
```json
{
  "code": 100,
  "message": "错误信息"
}
```

## 认证令牌使用

登录成功后，API会返回一个JWT令牌。在后续的API请求中，需要在请求头中包含：

```
Authorization: Bearer <token>
```

## 错误处理

脚本包含完整的错误处理机制：

- 网络连接错误
- 服务器错误
- 认证失败
- 参数验证错误

## 配置说明

编辑 `config.yaml` 文件来修改配置：

```yaml
api:
  base_url: "http://localhost:9380"  # API服务器地址
  timeout: 30                         # 请求超时时间
  headers:
    Content-Type: "application/json"
    Accept: "application/json"

output:
  format: "table"  # 输出格式：table, json, yaml
  max_width: 120

logging:
  level: "INFO"    # 日志级别
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

## 故障排除

### 1. 连接失败
- 检查RAGForge服务器是否运行
- 确认API地址是否正确
- 检查防火墙设置

### 2. 认证失败
- 确认用户名和密码正确
- 检查用户是否已注册
- 确认API端点路径正确

### 3. 权限错误
- 确认用户有相应权限
- 检查认证令牌是否有效
- 确认令牌格式正确

## 开发说明

### 添加新的API调用

1. 在 `api_client.py` 中添加新的方法
2. 在相应的脚本中调用新方法
3. 添加错误处理和日志记录

### 扩展功能

- 添加密码重置功能
- 支持多用户管理
- 添加API调用统计
- 支持批量操作

## 安全注意事项

1. **不要硬编码密码** - 使用环境变量或配置文件
2. **保护认证令牌** - 不要在日志中输出完整令牌
3. **使用HTTPS** - 生产环境中使用HTTPS连接
4. **定期更新令牌** - 定期刷新认证令牌
5. **输入验证** - 验证所有用户输入

## 示例用法

### 在Python脚本中使用

```python
from user_auth import UserAuth

# 创建认证实例
auth = UserAuth("http://localhost:9380")

# 注册用户
success, message = auth.register_user("test@example.com", "password123", "testuser")

# 登录用户
success, message, token = auth.login_user("test@example.com", "password123")

# 使用认证令牌调用其他API
if token:
    # 设置认证令牌
    auth.api_client.set_auth_token(token)
    
    # 调用需要认证的API
    # response = auth.api_client.get("/v1/datasets")
```

### 在Shell脚本中使用

```bash
#!/bin/bash

# 注册用户
python user_auth.py register

# 登录用户
python user_auth.py login

# 调用其他API
curl -H "Authorization: Bearer $TOKEN" http://localhost:9380/v1/datasets
``` 