import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def system():
    """系统管理命令"""
    pass


@system.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def status(output_format):
    """获取系统状态"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/v1/system/status')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "系统状态")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取系统状态失败: {e}")


@system.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def version(output_format):
    """获取系统版本信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/v1/system/version')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "系统版本信息")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取系统版本失败: {e}")


@system.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def config(output_format):
    """获取系统配置"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/v1/system/config')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "系统配置")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取系统配置失败: {e}")


@system.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def interface_config(output_format):
    """获取接口配置"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/v1/system/interface/config')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "接口配置")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取接口配置失败: {e}")


@system.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def upload_interface(file_path, output_format):
    """上传接口文件"""
    try:
        import os
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            formatter.print_error(f"文件不存在: {file_path}")
            return
        
        # 读取文件内容
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'application/octet-stream')}
            
            # 调用API
            response = client.post('/v1/system/interface/upload', files=files)
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "文件上传结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"文件上传失败: {e}")


@system.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def new_token(output_format):
    """生成新的API令牌"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.post('/v1/system/new_token')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "新API令牌")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"生成新令牌失败: {e}")


@system.command()
@click.argument('token')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def token_info(token, output_format):
    """获取令牌信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get(f'/v1/system/token/{token}')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "令牌信息")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取令牌信息失败: {e}")


@system.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def token_list(output_format):
    """获取令牌列表"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/v1/system/token_list')
        
        # 格式化输出
        if output_format == 'table':
            if isinstance(response, dict) and 'tokens' in response:
                formatter.print_rich_table(response['tokens'], "令牌列表")
            else:
                formatter.print_rich_table([response], "令牌列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取令牌列表失败: {e}") 