#!/usr/bin/env python3
"""
检查API状态的脚本
"""

import requests
import json

def check_api_status():
    base_url = "http://localhost:9380"
    
    print("🔍 检查RAGForge API状态...")
    
    # 1. 检查基本连接
    try:
        response = requests.get(f"{base_url}/v1/system/status", timeout=5)
        print(f"✅ 基本连接成功 (状态码: {response.status_code})")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 基本连接失败: {e}")
    
    # 2. 检查API文档
    try:
        response = requests.get(f"{base_url}/apispec.json", timeout=5)
        print(f"\n✅ API文档获取成功 (状态码: {response.status_code})")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   API版本: {data.get('info', {}).get('version', 'Unknown')}")
            print(f"   API标题: {data.get('info', {}).get('title', 'Unknown')}")
    except Exception as e:
        print(f"❌ API文档获取失败: {e}")
    
    # 3. 检查是否需要认证
    try:
        response = requests.get(f"{base_url}/v1/user/info", timeout=5)
        print(f"\n📋 用户信息检查 (状态码: {response.status_code})")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if data.get('code') == 100:
                print("   ⚠️  需要认证")
            elif data.get('code') == 401:
                print("   ❌ 未认证")
            else:
                print("   ✅ 已认证")
    except Exception as e:
        print(f"❌ 用户信息检查失败: {e}")
    
    # 4. 检查数据集API
    try:
        response = requests.get(f"{base_url}/api/v1/datasets", timeout=5)
        print(f"\n📊 数据集API检查 (状态码: {response.status_code})")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if data.get('code') == 100:
                print("   ⚠️  需要认证")
            elif data.get('code') == 401:
                print("   ❌ 未认证")
            else:
                print("   ✅ 可以访问数据集")
    except Exception as e:
        print(f"❌ 数据集API检查失败: {e}")

if __name__ == "__main__":
    check_api_status() 