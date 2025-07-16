#!/usr/bin/env python3
"""
RAGForge Shell客户端快速启动脚本
提供简单的命令行界面
"""

import sys
import os
from user_auth import UserAuth, interactive_register, interactive_login


def show_menu():
    """显示主菜单"""
    print("\n🚀 RAGForge Shell客户端")
    print("=" * 40)
    print("1. 用户注册")
    print("2. 用户登录")
    print("3. 用户登出")
    print("4. 测试API连接")
    print("5. 运行示例")
    print("6. 查看帮助")
    print("0. 退出")
    print("=" * 40)


def test_connection():
    """测试API连接"""
    print("\n🔍 测试API连接...")
    auth = UserAuth()
    
    if auth.check_server_status():
        print("✅ 服务器连接正常")
        print("   API地址: http://localhost:9380")
        
        # 获取系统配置
        try:
            response = requests.get("http://localhost:9380/v1/system/config", timeout=5)
            if response.status_code == 200:
                data = response.json()
                register_enabled = data.get('data', {}).get('registerEnabled', 0)
                print(f"   用户注册: {'启用' if register_enabled else '禁用'}")
        except:
            pass
    else:
        print("❌ 无法连接到服务器")
        print("   请确保RAGForge服务器正在运行")
        print("   默认地址: http://localhost:9380")


def show_help():
    """显示帮助信息"""
    print("\n📖 使用帮助")
    print("=" * 40)
    print("RAGForge Shell客户端是一个命令行工具，用于与RAGForge API交互。")
    print()
    print("主要功能:")
    print("• 用户注册和登录")
    print("• API调用和测试")
    print("• 批量操作")
    print()
    print("常用命令:")
    print("• python user_auth.py register  # 注册用户")
    print("• python user_auth.py login     # 用户登录")
    print("• python test_auth_endpoints.py # 测试API端点")
    print("• python example_usage.py       # 运行示例")
    print()
    print("配置文件: config.yaml")
    print("日志文件: 控制台输出")


def main():
    """主函数"""
    auth = UserAuth()
    
    while True:
        show_menu()
        
        try:
            choice = input("\n请选择操作 (0-6): ").strip()
            
            if choice == "1":
                print("\n📝 用户注册")
                interactive_register()
                
            elif choice == "2":
                print("\n🔐 用户登录")
                interactive_login()
                
            elif choice == "3":
                print("\n🔓 用户登出")
                auth.logout()
                
            elif choice == "4":
                test_connection()
                
            elif choice == "5":
                print("\n📦 运行示例...")
                try:
                    from example_usage import example_user_management
                    example_user_management()
                except ImportError:
                    print("❌ 示例模块未找到")
                except Exception as e:
                    print(f"❌ 运行示例时出错: {e}")
                    
            elif choice == "6":
                show_help()
                
            elif choice == "0":
                print("\n👋 再见!")
                break
                
            else:
                print("❌ 无效选择，请重新输入")
                
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，再见!")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")


if __name__ == "__main__":
    main() 