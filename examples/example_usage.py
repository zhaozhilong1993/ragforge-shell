#!/usr/bin/env python3
"""
RAGForge Shell客户端使用示例
演示用户注册、登录和API调用
"""

import requests
import json
from user_auth import UserAuth
from password_utils import encrypt_password


def example_user_management():
    """用户管理示例"""
    print("🚀 RAGForge Shell客户端使用示例")
    print("=" * 50)
    
    # 创建认证实例
    auth = UserAuth("http://localhost:9380")
    
    # 检查服务器状态
    print("\n1. 检查服务器状态...")
    if auth.check_server_status():
        print("✅ 服务器连接正常")
    else:
        print("❌ 无法连接到服务器")
        return
    
    # 示例用户信息
    test_email = "demo@example.com"
    test_password = "demo123456"
    test_nickname = "Demo User"
    
    print(f"\n2. 注册用户: {test_email}")
    success, message = auth.register_user(test_email, test_password, test_nickname)
    
    if success:
        print("✅ 用户注册成功")
    else:
        print(f"⚠️  注册结果: {message}")
    
    print(f"\n3. 登录用户: {test_email}")
    success, message, token = auth.login_user(test_email, test_password)
    
    if success:
        print("✅ 用户登录成功")
        print(f"   认证令牌: {token[:30]}...")
        
        # 获取用户信息
        print("\n4. 获取用户信息...")
        user_info = auth.get_current_user()
        if user_info:
            print(f"   用户ID: {user_info.get('id')}")
            print(f"   昵称: {user_info.get('nickname')}")
            print(f"   邮箱: {user_info.get('email')}")
            print(f"   语言: {user_info.get('language')}")
            print(f"   时区: {user_info.get('timezone')}")
        
        # 登出
        print("\n5. 用户登出...")
        auth.logout()
        print("✅ 用户已登出")
        
    else:
        print(f"❌ 登录失败: {message}")


def example_api_calls():
    """API调用示例"""
    print("\n🔧 API调用示例")
    print("=" * 30)
    
    # 首先登录
    auth = UserAuth("http://localhost:9380")
    success, message, token = auth.login_user("test@example.com.cn", "test123")
    
    if not success:
        print("❌ 登录失败，无法进行API调用")
        return
    
    print("✅ 登录成功，开始API调用...")
    
    # 示例1: 获取系统配置
    print("\n1. 获取系统配置...")
    try:
        response = requests.get(
            "http://localhost:9380/v1/system/config",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   注册功能: {'启用' if data.get('data', {}).get('registerEnabled') else '禁用'}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 示例2: 获取知识库列表
    print("\n2. 获取知识库列表...")
    try:
        response = requests.get(
            "http://localhost:9380/v1/kb/list",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            kb_count = len(data.get('data', []))
            print(f"   知识库数量: {kb_count}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
    
    # 示例3: 获取LLM工厂列表
    print("\n3. 获取LLM工厂列表...")
    try:
        response = requests.get(
            "http://localhost:9380/v1/llm/factories",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            factory_count = len(data.get('data', []))
            print(f"   LLM工厂数量: {factory_count}")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")


def example_batch_operations():
    """批量操作示例"""
    print("\n📦 批量操作示例")
    print("=" * 30)
    
    # 创建多个测试用户
    test_users = [
        {"email": "user1@example.com", "password": "pass123", "nickname": "User 1"},
        {"email": "user2@example.com", "password": "pass123", "nickname": "User 2"},
        {"email": "user3@example.com", "password": "pass123", "nickname": "User 3"},
    ]
    
    auth = UserAuth("http://localhost:9380")
    
    print("批量注册用户...")
    for i, user in enumerate(test_users, 1):
        print(f"   {i}. 注册用户: {user['email']}")
        success, message = auth.register_user(user['email'], user['password'], user['nickname'])
        if success:
            print(f"      ✅ 成功")
        else:
            print(f"      ⚠️  {message}")
    
    print("\n批量登录测试...")
    for i, user in enumerate(test_users, 1):
        print(f"   {i}. 登录用户: {user['email']}")
        success, message, token = auth.login_user(user['email'], user['password'])
        if success:
            print(f"      ✅ 成功")
        else:
            print(f"      ❌ {message}")


def main():
    """主函数"""
    print("选择示例:")
    print("1. 用户管理示例")
    print("2. API调用示例")
    print("3. 批量操作示例")
    print("4. 运行所有示例")
    
    choice = input("\n请输入选择 (1-4): ").strip()
    
    if choice == "1":
        example_user_management()
    elif choice == "2":
        example_api_calls()
    elif choice == "3":
        example_batch_operations()
    elif choice == "4":
        example_user_management()
        example_api_calls()
        example_batch_operations()
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    main() 