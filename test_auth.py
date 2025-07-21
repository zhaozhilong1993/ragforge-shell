#!/usr/bin/env python3
"""
测试不同认证格式的脚本
"""

import requests
import json

def test_auth_formats():
    """测试不同的认证格式"""
    base_url = "http://localhost:9380"
    endpoint = "/api/v1/datasets/123/documents"
    
    # 从配置文件读取token
    with open('config.yaml', 'r') as f:
        import yaml
        config = yaml.safe_load(f)
    
    api_token = config['api']['api_token']
    auth_token = config['api']['auth_token']
    
    print("测试不同的认证格式...")
    print(f"API Token: {api_token}")
    print(f"Auth Token: {auth_token}")
    print()
    
    # 测试1: 使用Bearer格式的API token
    headers1 = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }
    
    print("测试1: Bearer API Token")
    try:
        response1 = requests.get(f"{base_url}{endpoint}", headers=headers1, timeout=30)
        print(f"状态码: {response1.status_code}")
        print(f"响应: {response1.text}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()
    
    # 测试2: 直接使用API token
    headers2 = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': api_token
    }
    
    print("测试2: 直接API Token")
    try:
        response2 = requests.get(f"{base_url}{endpoint}", headers=headers2, timeout=30)
        print(f"状态码: {response2.status_code}")
        print(f"响应: {response2.text}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()
    
    # 测试3: 使用auth token
    headers3 = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': auth_token
    }
    
    print("测试3: Auth Token")
    try:
        response3 = requests.get(f"{base_url}{endpoint}", headers=headers3, timeout=30)
        print(f"状态码: {response3.status_code}")
        print(f"响应: {response3.text}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()
    
    # 测试4: 使用Bearer格式的auth token
    headers4 = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }
    
    print("测试4: Bearer Auth Token")
    try:
        response4 = requests.get(f"{base_url}{endpoint}", headers=headers4, timeout=30)
        print(f"状态码: {response4.status_code}")
        print(f"响应: {response4.text}")
        print()
    except Exception as e:
        print(f"错误: {e}")
        print()

if __name__ == "__main__":
    test_auth_formats() 