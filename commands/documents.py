import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def documents():
    """文档管理命令"""
    pass


@documents.command()
@click.argument('dataset_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def list(dataset_id, output_format):
    """列出数据集中的所有文档"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get(f'/api/v1/datasets/{dataset_id}/documents')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table(response.get('documents', []), f"数据集 {dataset_id} 的文档列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取文档列表失败: {e}")


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
        
        # 构建请求数据
        document_data = {
            'name': name
        }
        
        if content:
            document_data['content'] = content
        
        # 调用API
        response = client.post(f'/api/v1/datasets/{dataset_id}/documents', 
                             json_data={'document': document_data})
        
        formatter.print_success(f"文档 {name} 创建成功")
        
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