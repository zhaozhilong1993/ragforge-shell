import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def storage():
    """存储服务命令"""
    pass


@storage.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def volume_list(output_format):
    """列出所有存储卷"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/api/v1/volumes')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table(response.get('volumes', []), "存储卷列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取存储卷列表失败: {e}")


@storage.command()
@click.argument('volume_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def volume_show(volume_id, output_format):
    """显示存储卷详细信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get(f'/api/v1/volumes/{volume_id}')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], f"存储卷 {volume_id} 详情")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取存储卷详情失败: {e}")


@storage.command()
@click.argument('name')
@click.option('--size', required=True, type=int, help='存储卷大小(GB)')
@click.option('--type', 'volume_type', help='存储卷类型')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def volume_create(name, size, volume_type, output_format):
    """创建新存储卷"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建请求数据
        volume_data = {
            'name': name,
            'size': size
        }
        
        if volume_type:
            volume_data['volume_type'] = volume_type
        
        # 调用API
        response = client.post('/api/v1/volumes', json_data={'volume': volume_data})
        
        formatter.print_success(f"存储卷 {name} 创建成功")
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('volume', {})], "创建的存储卷")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"创建存储卷失败: {e}")


@storage.command()
@click.argument('volume_id')
def volume_delete(volume_id):
    """删除存储卷"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 调用API
        client.delete(f'/api/v1/volumes/{volume_id}')
        
        formatter.print_success(f"存储卷 {volume_id} 删除成功")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"删除存储卷失败: {e}")


@storage.command()
@click.argument('volume_id')
@click.argument('server_id')
def volume_attach(volume_id, server_id):
    """将存储卷挂载到服务器"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 构建请求数据
        attach_data = {
            'volumeAttachment': {
                'volumeId': volume_id,
                'serverId': server_id
            }
        }
        
        # 调用API
        response = client.post(f'/api/v1/servers/{server_id}/os-volume_attachments', 
                             json_data=attach_data)
        
        formatter.print_success(f"存储卷 {volume_id} 挂载到服务器 {server_id} 成功")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"挂载存储卷失败: {e}")


@storage.command()
@click.argument('volume_id')
@click.argument('server_id')
def volume_detach(volume_id, server_id):
    """从服务器卸载存储卷"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 调用API
        client.delete(f'/api/v1/servers/{server_id}/os-volume_attachments/{volume_id}')
        
        formatter.print_success(f"存储卷 {volume_id} 从服务器 {server_id} 卸载成功")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"卸载存储卷失败: {e}")


@storage.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def snapshot_list(output_format):
    """列出所有快照"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get('/api/v1/snapshots')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table(response.get('snapshots', []), "快照列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取快照列表失败: {e}")


@storage.command()
@click.argument('volume_id')
@click.argument('name')
@click.option('--description', help='快照描述')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def snapshot_create(volume_id, name, description, output_format):
    """创建存储卷快照"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建请求数据
        snapshot_data = {
            'name': name,
            'volume_id': volume_id
        }
        
        if description:
            snapshot_data['description'] = description
        
        # 调用API
        response = client.post('/api/v1/snapshots', json_data={'snapshot': snapshot_data})
        
        formatter.print_success(f"存储卷 {volume_id} 的快照 {name} 创建成功")
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('snapshot', {})], "创建的快照")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"创建快照失败: {e}") 