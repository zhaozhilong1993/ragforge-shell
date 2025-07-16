import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


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
        client = APIClient()
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
        client = APIClient()
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
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建登录数据
        login_data = {
            'email': email,
            'password': password
        }
        
        # 调用API
        response = client.post('/v1/user/login', json_data=login_data)
        
        formatter.print_success("登录成功")
        
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
        client = APIClient()
        formatter = OutputFormatter()
        
        # 调用API
        response = client.get('/v1/user/logout')
        
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
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建注册数据
        register_data = {
            'email': email,
            'password': password,
            'nickname': nickname
        }
        
        # 调用API
        response = client.post('/v1/user/register', json_data=register_data)
        
        formatter.print_success("注册成功")
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "注册结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"注册失败: {e}") 