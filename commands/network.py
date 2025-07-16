import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def network():
    """网络服务命令"""
    pass


@network.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def list(output_format):
    """列出所有网络"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/api/v1/networks')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table(response.get('networks', []), "网络列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取网络列表失败: {e}")


@network.command()
@click.argument('network_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def show(network_id, output_format):
    """显示网络详细信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get(f'/api/v1/networks/{network_id}')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], f"网络 {network_id} 详情")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取网络详情失败: {e}")


@network.command()
@click.argument('name')
@click.option('--subnet', help='子网CIDR')
@click.option('--gateway', help='网关IP')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def create(name, subnet, gateway, output_format):
    """创建新网络"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建请求数据
        network_data = {
            'name': name
        }
        
        if subnet:
            network_data['subnet'] = subnet
        if gateway:
            network_data['gateway'] = gateway
        
        # 调用API
        response = client.post('/api/v1/networks', json_data={'network': network_data})
        
        formatter.print_success(f"网络 {name} 创建成功")
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('network', {})], "创建的网络")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"创建网络失败: {e}")


@network.command()
@click.argument('network_id')
def delete(network_id):
    """删除网络"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 调用API
        client.delete(f'/api/v1/networks/{network_id}')
        
        formatter.print_success(f"网络 {network_id} 删除成功")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"删除网络失败: {e}")


@network.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def subnet_list(output_format):
    """列出所有子网"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/api/v1/subnets')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table(response.get('subnets', []), "子网列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取子网列表失败: {e}")


@network.command()
@click.argument('subnet_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def subnet_show(subnet_id, output_format):
    """显示子网详细信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get(f'/api/v1/subnets/{subnet_id}')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], f"子网 {subnet_id} 详情")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取子网详情失败: {e}") 