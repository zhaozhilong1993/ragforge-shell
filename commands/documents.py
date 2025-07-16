import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def documents():
    """文档管理命令"""
    pass


@documents.command(name='list')
@click.argument('dataset_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml', 'simple']), 
              help='输出格式')
def list_documents(dataset_id, output_format):
    """列出数据集中的所有文档"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 自动兼容token
        if not _ensure_token(client, formatter):
            return
        
        # 调用API
        response = client.get(f'/api/v1/datasets/{dataset_id}/documents')
        
        # 如果返回认证错误，尝试切换token格式
        if response.get('message') == 'Please check your authorization format.':
            # 切换token格式重试
            auth_token = client.config.get('api', {}).get('auth_token')
            api_token = client.config.get('api', {}).get('api_token')
            
            if auth_token and api_token:
                # 如果当前是auth_token，切换到api_token
                if client.session.headers.get('Authorization') == auth_token:
                    client.session.headers['Authorization'] = f"Bearer {api_token}"
                else:
                    client.session.headers['Authorization'] = auth_token
                
                # 重试请求
                response = client.get(f'/api/v1/datasets/{dataset_id}/documents')
        
        docs = response.get('documents')
        if docs is None or docs is False or docs == {}:
            docs = response.get('data')
        # 兼容重试后返回{'docs': [], 'total': 0}
        if isinstance(docs, dict) and 'docs' in docs:
            docs = docs['docs']
        if not isinstance(docs, list):
            docs = []
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table(docs, f"数据集 {dataset_id} 的文档列表")
        elif output_format == 'simple':
            formatter.print_simple_list(docs, f"数据集 {dataset_id} 的文档列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取文档列表失败: {e}")
        # 输出详细错误信息
        if hasattr(e, 'response') and e.response:
            formatter.print_error(f"API响应: {e.response.text}")


@documents.command()
@click.argument('dataset_id')
@click.argument('document_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def show(dataset_id, document_id, output_format):
    """显示文档详细信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        if not _ensure_token(client, formatter):
            return

        # 调用API
        response = client.get(f'/api/v1/datasets/{dataset_id}/documents/{document_id}')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], f"文档 {document_id} 详情")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取文档详情失败: {e}")


@documents.command()
@click.argument('dataset_id')
@click.argument('name')
@click.option('--content', help='文档内容')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def create(dataset_id, name, content, output_format):
    """在数据集中创建新文档"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        if not _ensure_token(client, formatter):
            return

        # 构建请求数据
        document_data = {
            'name': name
        }
        
        if content:
            document_data['content'] = content
        
        # 调用API
        response = client.post(f'/api/v1/datasets/{dataset_id}/documents', 
                             json_data={'document': document_data})
        
        # 检查API响应是否真正成功
        if response.get('code') == 0 and not response.get('message', '').startswith('Please check your authorization'):
            formatter.print_success(f"文档 {name} 创建成功")
        else:
            error_msg = response.get('message', '未知错误')
            formatter.print_error(f"创建文档失败: {error_msg}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('document', {})], "创建的文档")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"创建文档失败: {e}")


@documents.command()
@click.argument('dataset_id')
@click.argument('document_id')
def delete(dataset_id, document_id):
    """删除文档"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 检查是否有API token
        if not _ensure_token(client, formatter):
            return

        # 调用API
        client.delete(f'/api/v1/datasets/{dataset_id}/documents/{document_id}')
        
        formatter.print_success(f"文档 {document_id} 删除成功")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"删除文档失败: {e}")


@documents.command()
@click.argument('dataset_id')
@click.argument('document_id')
@click.argument('name')
@click.option('--content', help='新的文档内容')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def update(dataset_id, document_id, name, content, output_format):
    """更新文档信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        if not _ensure_token(client, formatter):
            return

        # 构建请求数据
        update_data = {
            'name': name
        }
        
        if content:
            update_data['content'] = content
        
        # 调用API
        response = client.put(f'/api/v1/datasets/{dataset_id}/documents/{document_id}', 
                            json_data={'document': update_data})
        
        formatter.print_success(f"文档 {document_id} 更新成功")
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "更新后的文档")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"更新文档失败: {e}")


@documents.command()
@click.argument('dataset_id')
@click.argument('document_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def chunks(dataset_id, document_id, output_format):
    """列出文档的所有块"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        if not _ensure_token(client, formatter):
            return

        # 调用API
        response = client.get(f'/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table(response.get('chunks', []), f"文档 {document_id} 的块列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取文档块列表失败: {e}") 


def _ensure_token(client, formatter):
    """自动兼容两种token方式"""
    # 优先尝试 auth_token（直接token）
    auth_token = client.config.get('api', {}).get('auth_token')
    if auth_token:
        client.session.headers['Authorization'] = auth_token
        return True
    
    # 备选 api_token（Bearer格式）
    api_token = client.config.get('api', {}).get('api_token')
    if api_token:
        client.session.headers['Authorization'] = f"Bearer {api_token}"
        return True
    
    formatter.print_error("未找到API令牌，请先登录")
    return False 