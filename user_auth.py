#!/usr/bin/env python3
"""
RAGForge 用户认证脚本
支持用户注册和登录功能
"""

import requests
import json
import sys
import getpass
from typing import Dict, Optional, Tuple
from api_client import APIClient
from password_utils import encrypt_password


class UserAuth:
    """用户认证类"""
    
    def __init__(self, base_url: str = "http://localhost:9380"):
        self.base_url = base_url.rstrip('/')
        self.api_client = APIClient()
        self.current_user = None
        self.auth_token = None
    
    def register_user(self, email: str, password: str, nickname: str) -> Tuple[bool, str]:
        """
        注册新用户
        
        Args:
            email: 用户邮箱
            password: 用户密码
            nickname: 用户昵称（必需）
            
        Returns:
            (success, message)
        """
        try:
            # 加密密码
            encrypted_password = encrypt_password(password)
            
            # 构建注册数据 - 根据API代码，需要nickname字段
            register_data = {
                "email": email,
                "password": encrypted_password,
                "nickname": nickname
            }
            
            print(f"📝 正在注册用户: {email}")
            
            response = requests.post(
                f"{self.base_url}/v1/user/register",
                json=register_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    print("✅ 用户注册成功!")
                    return True, "注册成功"
                else:
                    error_msg = data.get('message', '注册失败')
                    print(f"❌ 注册失败: {error_msg}")
                    return False, error_msg
            else:
                error_msg = f"HTTP错误: {response.status_code}"
                print(f"❌ {error_msg}")
                return False, error_msg
                
        except requests.exceptions.ConnectionError:
            error_msg = "无法连接到服务器，请检查API服务是否启动"
            print(f"❌ {error_msg}")
            return False, error_msg
        except Exception as e:
            error_msg = f"注册过程中发生错误: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def login_user(self, email: str, password: str) -> Tuple[bool, str, Optional[str]]:
        """
        用户登录
        
        Args:
            email: 用户邮箱
            password: 用户密码
            
        Returns:
            (success, message, token)
        """
        try:
            print(f"🔐 正在登录: {email}")
            
            # 加密密码
            encrypted_password = encrypt_password(password)
            
            login_data = {
                "email": email,
                "password": encrypted_password
            }
            
            response = requests.post(
                f"{self.base_url}/v1/user/login",
                json=login_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    # 登录成功
                    user_info = data.get('data', {})
                    token = user_info.get('access_token')  # 根据API代码，字段名是access_token
                    nickname = user_info.get('nickname', email)
                    
                    if token:
                        self.auth_token = token
                        self.current_user = {
                            'email': email,
                            'nickname': nickname,
                            'token': token
                        }
                        self.api_client.set_auth_token(token)
                        
                        print("✅ 登录成功!")
                        print(f"   用户: {nickname}")
                        print(f"   邮箱: {email}")
                        return True, "登录成功", token
                    else:
                        error_msg = "登录响应中没有找到认证令牌"
                        print(f"❌ {error_msg}")
                        return False, error_msg, None
                else:
                    error_msg = data.get('message', '登录失败')
                    print(f"❌ 登录失败: {error_msg}")
                    return False, error_msg, None
            else:
                error_msg = f"HTTP错误: {response.status_code}"
                print(f"❌ {error_msg}")
                return False, error_msg, None
                
        except requests.exceptions.ConnectionError:
            error_msg = "无法连接到服务器，请检查API服务是否启动"
            print(f"❌ {error_msg}")
            return False, error_msg, None
        except Exception as e:
            error_msg = f"登录过程中发生错误: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg, None
    
    def logout(self) -> bool:
        """用户登出"""
        if not self.auth_token:
            print("⚠️  当前没有登录用户")
            return False
        
        try:
            print("🔓 正在登出...")
            
            response = requests.get(  # 根据API代码，logout是GET请求
                f"{self.base_url}/v1/user/logout",
                headers={
                    "Authorization": f"Bearer {self.auth_token}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ 登出成功!")
                self.current_user = None
                self.auth_token = None
                self.api_client.clear_auth_token()
                return True
            else:
                print(f"❌ 登出失败: HTTP {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ 登出过程中发生错误: {str(e)}")
            return False
    
    def get_current_user(self) -> Optional[Dict]:
        """获取当前用户信息"""
        if not self.auth_token:
            return None
        
        try:
            response = requests.get(
                f"{self.base_url}/v1/user/info",  # 根据API代码，用户信息端点是/info
                headers={
                    "Authorization": f"Bearer {self.auth_token}"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('code') == 0:
                    return data.get('data')
            
            return None
            
        except Exception:
            return None
    
    def check_server_status(self) -> bool:
        """检查服务器状态"""
        try:
            response = requests.get(f"{self.base_url}/v1/system/config", timeout=5)
            return response.status_code == 200
        except:
            return False


def interactive_register():
    """交互式用户注册"""
    print("🚀 RAGForge 用户注册")
    print("=" * 40)
    
    auth = UserAuth()
    
    # 检查服务器状态
    if not auth.check_server_status():
        print("❌ 无法连接到RAGForge服务器")
        print("   请确保服务器正在运行: http://localhost:9380")
        return False
    
    # 获取用户输入
    email = input("📧 邮箱地址: ").strip()
    if not email:
        print("❌ 邮箱地址不能为空")
        return False
    
    password = getpass.getpass("🔒 密码: ")
    if not password:
        print("❌ 密码不能为空")
        return False
    
    confirm_password = getpass.getpass("🔒 确认密码: ")
    if password != confirm_password:
        print("❌ 两次输入的密码不一致")
        return False
    
    nickname = input("👤 用户昵称: ").strip()
    if not nickname:
        print("❌ 用户昵称不能为空")
        return False
    
    # 执行注册
    success, message = auth.register_user(email, password, nickname)
    
    if success:
        print("\n✅ 注册成功! 现在可以登录了")
        return True
    else:
        print(f"\n❌ 注册失败: {message}")
        return False


def interactive_login():
    """交互式用户登录"""
    print("🔐 RAGForge 用户登录")
    print("=" * 40)
    
    auth = UserAuth()
    
    # 检查服务器状态
    if not auth.check_server_status():
        print("❌ 无法连接到RAGForge服务器")
        print("   请确保服务器正在运行: http://localhost:9380")
        return False
    
    # 获取用户输入
    email = input("📧 邮箱地址: ").strip()
    if not email:
        print("❌ 邮箱地址不能为空")
        return False
    
    password = getpass.getpass("🔒 密码: ")
    if not password:
        print("❌ 密码不能为空")
        return False
    
    # 执行登录
    success, message, token = auth.login_user(email, password)
    
    if success:
        print(f"\n✅ 登录成功! 认证令牌: {token[:20]}...")
        return True
    else:
        print(f"\n❌ 登录失败: {message}")
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python user_auth.py register  # 注册新用户")
        print("  python user_auth.py login     # 用户登录")
        print("  python user_auth.py logout    # 用户登出")
        return
    
    command = sys.argv[1].lower()
    auth = UserAuth()
    
    if command == "register":
        interactive_register()
    elif command == "login":
        interactive_login()
    elif command == "logout":
        auth.logout()
    else:
        print(f"❌ 未知命令: {command}")
        print("可用命令: register, login, logout")


if __name__ == "__main__":
    main() 