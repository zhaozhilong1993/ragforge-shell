import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter
from password_utils import encrypt_password

# 全局认证状态管理
_auth_client = None

def get_auth_client():
    """获取认证客户端实例"""
    global _auth_client
    if _auth_client is None:
        _auth_client = APIClient()
    return _auth_client

def set_auth_client(client):
    """设置认证客户端实例"""
    global _auth_client
    _auth_client = client


@click.group()
def user():
    """用户管理命令"""
    pass


@user.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def info(output_format):
    """获取当前用户信息"""
    try:
        client = get_auth_client()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/v1/user/info')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "当前用户信息")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取用户信息失败: {e}")


@user.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def tenant_info(output_format):
    """获取租户信息"""
    try:
        client = get_auth_client()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/v1/user/tenant_info')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "租户信息")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取租户信息失败: {e}")


@user.command()
@click.argument('email')
@click.argument('password')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def login(email, password, output_format):
    """用户登录"""
    try:
        client = get_auth_client()
        formatter = OutputFormatter(output_format)
        
        # 加密密码
        encrypted_password = encrypt_password(password)
        
        # 构建登录数据
        login_data = {
            'email': email,
            'password': encrypted_password
        }
        
        # 调用API
        response = client.post('/v1/user/login', json_data=login_data)
        
        if response.get('code') == 0:
            formatter.print_success("登录成功")
            
            # 检查是否有认证令牌
            auth_header = client.session.headers.get('Authorization')
            if auth_header:
                client.set_auth_token(auth_header)
                set_auth_client(client)  # 保存认证状态
                formatter.print_info(f"认证令牌: {auth_header[:20]}...")
                
                # 获取或创建API token
                try:
                    # 使用用户token调用API token创建接口
                    api_token_response = client.post('/v1/system/new_token')
                    if api_token_response.get('code') == 0:
                        api_token_data = api_token_response.get('data', {})
                        api_token = api_token_data.get('token')
                        if api_token:
                            # 保存API token到配置
                            if 'api' not in client.config:
                                client.config['api'] = {}
                            client.config['api']['api_token'] = api_token
                            client._save_config(client.config)
                            formatter.print_info(f"API令牌: {api_token[:20]}...")
                    else:
                        formatter.print_warning(f"获取API令牌失败: {api_token_response.get('message', '未知错误')}")
                except Exception as e:
                    formatter.print_warning(f"获取API令牌失败: {e}")
            else:
                formatter.print_warning("未找到认证令牌")
        else:
            formatter.print_error(f"登录失败: {response.get('message', '未知错误')}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "登录结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"登录失败: {e}")


@user.command()
def logout():
    """用户登出"""
    try:
        client = get_auth_client()
        formatter = OutputFormatter()
        
        # 调用API
        response = client.get('/v1/user/logout')
        
        # 清除认证令牌
        client.clear_auth_token()
        set_auth_client(client)  # 保存状态
        
        formatter.print_success("登出成功")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"登出失败: {e}")


@user.command()
@click.argument('email')
@click.argument('password')
@click.argument('nickname')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def register(email, password, nickname, output_format):
    """用户注册"""
    try:
        client = get_auth_client()
        formatter = OutputFormatter(output_format)
        
        # 加密密码
        encrypted_password = encrypt_password(password)
        
        # 构建注册数据
        register_data = {
            'email': email,
            'password': encrypted_password,
            'nickname': nickname
        }
        
        # 调用API
        response = client.post('/v1/user/register', json_data=register_data)
        
        if response.get('code') == 0:
            formatter.print_success("注册成功")
        else:
            formatter.print_error(f"注册失败: {response.get('message', '未知错误')}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "注册结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"注册失败: {e}")


@user.command()
@click.argument('email')
@click.argument('old_password')
@click.argument('new_password')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def reset_password(email, old_password, new_password, output_format):
    """重置用户密码"""
    try:
        client = get_auth_client()
        formatter = OutputFormatter(output_format)
        
        # 加密密码
        encrypted_old_password = encrypt_password(old_password)
        encrypted_new_password = encrypt_password(new_password)
        
        # 构建重置密码数据
        reset_data = {
            'email': email,
            'old_password': encrypted_old_password,
            'new_password': encrypted_new_password
        }
        
        # 调用API
        response = client.post('/v1/user/reset_password', json_data=reset_data)
        
        if response.get('code') == 0:
            formatter.print_success("密码重置成功")
        else:
            formatter.print_error(f"密码重置失败: {response.get('message', '未知错误')}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "密码重置结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"密码重置失败: {e}")


@user.command()
@click.argument('old_password')
@click.argument('new_password')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def change_password(old_password, new_password, output_format):
    """修改当前用户密码"""
    try:
        client = get_auth_client()
        formatter = OutputFormatter(output_format)
        
        # 检查是否已登录
        if not client.has_auth_token():
            formatter.print_error("请先登录")
            return
        
        # 加密密码
        encrypted_old_password = encrypt_password(old_password)
        encrypted_new_password = encrypt_password(new_password)
        
        # 构建修改密码数据
        change_data = {
            'old_password': encrypted_old_password,
            'new_password': encrypted_new_password
        }
        
        # 调用API
        response = client.post('/v1/user/change_password', json_data=change_data)
        
        if response.get('code') == 0:
            formatter.print_success("密码修改成功")
        else:
            formatter.print_error(f"密码修改失败: {response.get('message', '未知错误')}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "密码修改结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"密码修改失败: {e}")


@user.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def status(output_format):
    """检查用户认证状态"""
    try:
        client = get_auth_client()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有认证令牌
        if client.has_auth_token():
            formatter.print_success("已登录")
            
            # 尝试获取用户信息
            try:
                response = client.get('/v1/user/info')
                if response.get('code') == 0:
                    user_data = response.get('data', {})
                    formatter.print_info(f"用户: {user_data.get('nickname', 'Unknown')}")
                    formatter.print_info(f"邮箱: {user_data.get('email', 'Unknown')}")
                else:
                    formatter.print_warning("认证令牌可能已过期")
            except:
                formatter.print_warning("无法获取用户信息")
        else:
            formatter.print_info("未登录")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"检查认证状态失败: {e}") 