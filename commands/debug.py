import click
import json
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def debug():
    """调试命令"""
    pass


@debug.command()
@click.argument('endpoint')
@click.option('--method', default='GET', 
              type=click.Choice(['GET', 'POST', 'PUT', 'DELETE']), 
              help='HTTP方法')
@click.option('--data', help='请求数据(JSON格式)')
def test_api(endpoint, method, data):
    """测试API调用并显示详细信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        print(f"🔍 测试API调用:")
        print(f"   方法: {method}")
        print(f"   端点: {endpoint}")
        print(f"   基础URL: {client.base_url}")
        print(f"   完整URL: {client.base_url}{endpoint}")
        print(f"   请求头: {dict(client.session.headers)}")
        
        if data:
            print(f"   请求数据: {data}")
        
        print("\n📡 发送请求...")
        
        # 解析请求数据
        json_data = None
        if data:
            try:
                json_data = json.loads(data)
                print(f"   解析后的数据: {json.dumps(json_data, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError as e:
                formatter.print_error(f"JSON解析错误: {e}")
                return
        
        # 调用API
        try:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'POST':
                response = client.post(endpoint, json_data=json_data)
            elif method == 'PUT':
                response = client.put(endpoint, json_data=json_data)
            elif method == 'DELETE':
                response = client.delete(endpoint)
            
            print(f"✅ 请求成功!")
            print(f"   响应类型: {type(response)}")
            print(f"   响应内容: {json.dumps(response, indent=2, ensure_ascii=False)}")
            
        except Exception as e:
            print(f"❌ 请求失败: {e}")
            print(f"   错误类型: {type(e)}")
            
    except Exception as e:
        formatter.print_error(f"调试失败: {e}")


@debug.command()
def check_connection():
    """检查API连接状态"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        print("🔍 检查API连接...")
        print(f"   基础URL: {client.base_url}")
        print(f"   超时设置: {client.session.timeout}秒")
        print(f"   请求头: {dict(client.session.headers)}")
        
        # 测试基本连接
        try:
            print("\n📡 测试基本连接...")
            response = client.get('/v1/system/status')
            print("✅ 连接成功!")
            print(f"   系统状态: {json.dumps(response, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"❌ 连接失败: {e}")
        
        # 测试用户信息
        try:
            print("\n📡 测试用户信息...")
            response = client.get('/v1/user/info')
            print("✅ 用户信息获取成功!")
            print(f"   用户信息: {json.dumps(response, indent=2, ensure_ascii=False)}")
        except Exception as e:
            print(f"❌ 用户信息获取失败: {e}")
        
        # 测试数据集列表
        try:
            print("\n📡 测试数据集列表...")
            response = client.get('/api/v1/datasets')
            print("✅ 数据集列表获取成功!")
            print(f"   响应内容: {json.dumps(response, indent=2, ensure_ascii=False)}")
            
            if isinstance(response, dict) and 'datasets' in response:
                datasets = response['datasets']
                print(f"   数据集数量: {len(datasets)}")
                if datasets:
                    print("   数据集列表:")
                    for dataset in datasets:
                        print(f"     - {dataset.get('name', 'Unknown')} (ID: {dataset.get('id', 'Unknown')})")
                else:
                    print("   ⚠️  没有找到数据集")
            else:
                print("   ⚠️  响应格式不符合预期")
                
        except Exception as e:
            print(f"❌ 数据集列表获取失败: {e}")
            
    except Exception as e:
        formatter.print_error(f"连接检查失败: {e}")


@debug.command()
@click.argument('endpoint')
def raw_call(endpoint):
    """直接调用API并显示原始响应"""
    try:
        import requests
        
        client = APIClient()
        formatter = OutputFormatter()
        
        url = f"{client.base_url}{endpoint}"
        headers = dict(client.session.headers)
        
        print(f"🔍 原始API调用:")
        print(f"   URL: {url}")
        print(f"   方法: GET")
        print(f"   请求头: {json.dumps(headers, indent=2)}")
        
        print("\n📡 发送请求...")
        
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"   状态码: {response.status_code}")
        print(f"   响应头: {dict(response.headers)}")
        print(f"   响应内容:")
        print(response.text)
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                print(f"\n   解析后的JSON:")
                print(json.dumps(json_response, indent=2, ensure_ascii=False))
            except:
                print("   响应不是有效的JSON格式")
        else:
            print(f"   ❌ 请求失败，状态码: {response.status_code}")
            
    except Exception as e:
        formatter.print_error(f"原始调用失败: {e}") 