#!/usr/bin/env python3
"""
简单的API测试脚本
"""

import requests
import json
import time

def test_api():
    base_url = "http://localhost:9380"
    
    print("🔍 测试RAGForge API连接...")
    print(f"   基础URL: {base_url}")
    
    # 测试端点列表
    endpoints = [
        "/v1/system/status",
        "/v1/user/info", 
        "/api/v1/datasets",
        "/apispec.json"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n📡 测试端点: {endpoint}")
        print(f"   完整URL: {url}")
        
        try:
            # 设置请求头
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # 发送请求
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"   状态码: {response.status_code}")
            print(f"   响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
                except:
                    print(f"   响应内容: {response.text[:200]}...")
            else:
                print(f"   错误响应: {response.text}")
                
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ 连接错误: {e}")
        except requests.exceptions.Timeout as e:
            print(f"   ❌ 超时错误: {e}")
        except Exception as e:
            print(f"   ❌ 其他错误: {e}")
        
        time.sleep(1)  # 避免请求过快

if __name__ == "__main__":
    test_api() 