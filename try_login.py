#!/usr/bin/env python3
"""
尝试不同的登录方式
"""

import requests
import json

def try_different_logins():
    base_url = "http://localhost:9380"
    
    print("🔍 尝试不同的登录方式...")
    
    # 常见的测试账户
    test_accounts = [
        {"email": "admin@example.com", "password": "admin"},
        {"email": "admin@example.com", "password": "admin123"},
        {"email": "admin@example.com", "password": "password"},
        {"email": "test@example.com", "password": "test"},
        {"email": "test@example.com", "password": "test123"},
        {"email": "user@example.com", "password": "user"},
        {"email": "demo@example.com", "password": "demo"},
    ]
    
    for i, account in enumerate(test_accounts, 1):
        print(f"\n📝 尝试账户 {i}: {account['email']}")
        
        try:
            response = requests.post(
                f"{base_url}/v1/user/login",
                json=account,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   状态码: {response.status_code}")
                print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                if data.get('code') == 0:  # 成功
                    print("   ✅ 登录成功!")
                    return account
                else:
                    print(f"   ❌ 登录失败: {data.get('message', 'Unknown error')}")
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ 请求失败: {e}")
    
    print("\n❌ 所有登录尝试都失败了")
    return None

def check_system_info():
    base_url = "http://localhost:9380"
    
    print("\n🔍 检查系统信息...")
    
    # 检查版本
    try:
        response = requests.get(f"{base_url}/v1/system/version", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   系统版本: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"   版本检查失败: {e}")
    
    # 检查配置
    try:
        response = requests.get(f"{base_url}/v1/system/config", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   系统配置: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"   配置检查失败: {e}")

if __name__ == "__main__":
    check_system_info()
    successful_account = try_different_logins()
    
    if successful_account:
        print(f"\n✅ 找到可用的账户: {successful_account['email']}")
        print("   你可以在脚本中使用这个账户")
    else:
        print("\n❌ 没有找到可用的账户")
        print("   可能需要:")
        print("   1. 检查API服务器是否正确启动")
        print("   2. 查看API文档了解正确的登录方式")
        print("   3. 联系系统管理员获取正确的凭据") 