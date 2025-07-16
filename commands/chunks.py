import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def chunks():
    """文档块管理命令"""
    pass


@chunks.command()
@click.argument('dataset_id')
@click.argument('document_id')
@click.argument('chunk_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def show(dataset_id, document_id, chunk_id, output_format):
    """显示文档块详细信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 调用API
        response = client.get(f'/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}')
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], f"文档块 {chunk_id} 详情")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取文档块详情失败: {e}")


@chunks.command()
@click.argument('dataset_id')
@click.argument('document_id')
@click.argument('content')
@click.option('--keywords', help='重要关键词，用逗号分隔')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def add(dataset_id, document_id, content, keywords, output_format):
    """向文档添加新的块"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建请求数据
        chunk_data = {
            'content': content
        }
        
        if keywords:
            chunk_data['important_keywords'] = [kw.strip() for kw in keywords.split(',')]
        
        # 调用API
        response = client.post(f'/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks', 
                             json_data=chunk_data)
        
        formatter.print_success(f"文档块添加成功")
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('chunk', {})], "添加的文档块")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"添加文档块失败: {e}")


@chunks.command()
@click.argument('dataset_id')
@click.argument('document_id')
@click.argument('chunk_id')
@click.option('--content', help='更新的内容')
@click.option('--keywords', help='更新的重要关键词，用逗号分隔')
@click.option('--available', type=bool, help='可用性状态')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def update(dataset_id, document_id, chunk_id, content, keywords, available, output_format):
    """更新文档块"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建请求数据
        update_data = {}
        
        if content:
            update_data['content'] = content
        
        if keywords:
            update_data['important_keywords'] = [kw.strip() for kw in keywords.split(',')]
        
        if available is not None:
            update_data['available'] = available
        
        # 调用API
        response = client.put(f'/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}', 
                            json_data=update_data)
        
        formatter.print_success(f"文档块 {chunk_id} 更新成功")
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response], "更新后的文档块")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"更新文档块失败: {e}")


@chunks.command()
@click.argument('dataset_id')
@click.argument('document_id')
@click.argument('chunk_id')
def delete(dataset_id, document_id, chunk_id):
    """删除文档块"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 调用API
        client.delete(f'/api/v1/datasets/{dataset_id}/documents/{document_id}/chunks/{chunk_id}')
        
        formatter.print_success(f"文档块 {chunk_id} 删除成功")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"删除文档块失败: {e}") 