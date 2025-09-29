import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def datasets():
    """数据集管理命令"""
    pass


@datasets.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml', 'simple']), 
              help='输出格式')
def list(output_format):
    """列出所有数据集"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 调用API（使用API token的Bearer格式）
        response = client.get('/api/v1/datasets', headers={'Authorization': f"Bearer {api_token}"})
        
        # 格式化输出
        if output_format == 'table':
            datasets = response.get('data', [])
            if datasets:
                formatter.print_rich_table(datasets, "数据集列表")
            else:
                formatter.print_info("暂无数据集")
        elif output_format == 'simple':
            datasets = response.get('data', [])
            if datasets:
                formatter.print_simple_list(datasets, "数据集列表")
            else:
                formatter.print_info("暂无数据集")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取数据集列表失败: {e}")


@datasets.command()
@click.argument('dataset_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def show(dataset_id, output_format):
    """显示数据集详细信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 调用API（使用API token的Bearer格式）
        response = client.get(f'/api/v1/datasets/{dataset_id}', headers={'Authorization': f"Bearer {api_token}"})
        
        # 格式化输出
        if output_format == 'table':
            dataset = response.get('data', {})
            if dataset:
                formatter.print_rich_table([dataset], f"数据集 {dataset_id} 详情")
            else:
                formatter.print_error("数据集不存在")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取数据集详情失败: {e}")


@datasets.command()
@click.argument('name')
@click.option('--description', help='数据集描述')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def create(name, description, output_format):
    """创建新数据集"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 构建请求数据
        dataset_data = {
            'name': name
        }
        
        if description:
            dataset_data['description'] = description
        
        # 调用API（使用API token的Bearer格式）
        response = client.post('/api/v1/datasets', json_data=dataset_data, headers={'Authorization': f"Bearer {api_token}"})
        
        formatter.print_success(f"数据集 {name} 创建成功")
        
        # 格式化输出
        if output_format == 'table':
            dataset = response.get('data', {})
            if dataset:
                formatter.print_rich_table([dataset], "创建的数据集")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"创建数据集失败: {e}")


@datasets.command()
@click.argument('dataset_id')
def delete(dataset_id):
    """删除数据集"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 调用API（使用API token的Bearer格式）
        client.delete(f'/api/v1/datasets/{dataset_id}', headers={'Authorization': f"Bearer {api_token}"})
        
        formatter.print_success(f"数据集 {dataset_id} 删除成功")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"删除数据集失败: {e}")


@datasets.command()
@click.argument('dataset_id')
@click.argument('name')
@click.option('--description', help='新的数据集描述')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def update(dataset_id, name, description, output_format):
    """更新数据集信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 构建请求数据
        update_data = {
            'name': name
        }
        
        if description:
            update_data['description'] = description
        
        # 调用API（使用API token的Bearer格式）
        response = client.put(f'/api/v1/datasets/{dataset_id}', json_data=update_data, headers={'Authorization': f"Bearer {api_token}"})
        
        formatter.print_success(f"数据集 {dataset_id} 更新成功")
        
        # 格式化输出
        if output_format == 'table':
            dataset = response.get('data', {})
            if dataset:
                formatter.print_rich_table([dataset], "更新后的数据集")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"更新数据集失败: {e}") 