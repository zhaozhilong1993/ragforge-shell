#!/usr/bin/env python3
"""
测试RAGForge认证API端点
"""

import requests
import json
import sys
from password_utils import encrypt_password

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://localhost:9380"
    
    print("🔍 测试RAGForge API端点")
    print("=" * 50)
    
    # 测试服务器状态
    print("\n1. 测试服务器状态...")
    try:
        response = requests.get(f"{base_url}/v1/system/config", timeout=5)
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   ❌ 连接失败: {e}")
        return False
    
    # 测试用户注册端点
    print("\n2. 测试用户注册端点...")
    test_password = "test123"
    encrypted_password = encrypt_password(test_password)
    
    test_register_data = {
        "email": "test@example.com",
        "password": encrypted_password,
        "nickname": "testuser"  # 根据API代码，需要nickname字段
    }
    
    try:
        response = requests.post(
            f"{base_url}/v1/user/register",
            json=test_register_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    # 测试用户登录端点
    print("\n3. 测试用户登录端点...")
    test_login_data = {
        "email": "test@example.com",
        "password": encrypted_password
    }
    
    try:
        response = requests.post(
            f"{base_url}/v1/user/login",
            json=test_login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 如果登录成功，保存token用于后续测试
            if data.get('code') == 0:
                token = data.get('data', {}).get('access_token')  # 根据API代码，字段名是access_token
                if token:
                    print(f"   ✅ 获取到认证令牌: {token[:20]}...")
                    
                    # 测试获取用户信息
                    print("\n4. 测试获取用户信息...")
                    try:
                        response = requests.get(
                            f"{base_url}/v1/user/info",  # 根据API代码，用户信息端点是/info
                            headers={
                                "Authorization": f"Bearer {token}",
                                "Content-Type": "application/json"
                            },
                            timeout=10
                        )
                        print(f"   状态码: {response.status_code}")
                        if response.status_code == 200:
                            profile_data = response.json()
                            print(f"   响应: {json.dumps(profile_data, indent=2, ensure_ascii=False)}")
                        else:
                            print(f"   错误: {response.text}")
                    except Exception as e:
                        print(f"   ❌ 获取用户信息失败: {e}")
                    
                    # 测试登出
                    print("\n5. 测试用户登出...")
                    try:
                        response = requests.get(  # 根据API代码，logout是GET请求
                            f"{base_url}/v1/user/logout",
                            headers={
                                "Authorization": f"Bearer {token}"
                            },
                            timeout=10
                        )
                        print(f"   状态码: {response.status_code}")
                        if response.status_code == 200:
                            logout_data = response.json()
                            print(f"   响应: {json.dumps(logout_data, indent=2, ensure_ascii=False)}")
                        else:
                            print(f"   错误: {response.text}")
                    except Exception as e:
                        print(f"   ❌ 登出失败: {e}")
        else:
            print(f"   错误: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
    
    print("\n✅ API端点测试完成")
    return True

def check_available_endpoints():
    """检查可用的API端点"""
    base_url = "http://localhost:9380"
    
    print("\n🔍 检查可用的API端点...")
    
    # 根据实际API代码，更新端点列表
    endpoints = [
        "/v1/system/config",      # 系统配置
        "/v1/user/register",      # 用户注册
        "/v1/user/login",         # 用户登录
        "/v1/user/logout",        # 用户登出
        "/v1/user/info",          # 用户信息
        "/v1/tenant/list",        # 租户列表
        "/v1/kb/list",           # 知识库列表
        "/v1/llm/factories",     # LLM工厂列表
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            status = "✅" if response.status_code < 400 else "❌"
            print(f"   {status} {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} - 连接失败")

if __name__ == "__main__":
    test_api_endpoints()
    check_available_endpoints() 