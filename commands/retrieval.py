import click
from typing import Dict, Any, Optional
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def retrieval():
    """检索功能命令"""
    pass


@retrieval.command()
@click.argument('question')
@click.argument('dataset_ids', nargs=-1)
@click.option('--document-ids', help='文档ID列表，用逗号分隔')
@click.option('--top-k', type=int, default=10, help='返回的最大块数量')
@click.option('--similarity-threshold', type=float, help='相似度阈值')
@click.option('--vector-similarity-weight', type=float, help='向量相似度权重')
@click.option('--highlight', is_flag=True, help='是否高亮匹配内容')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def search(question, dataset_ids, document_ids, top_k, similarity_threshold, 
           vector_similarity_weight, highlight, output_format):
    """基于查询检索文档块"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建请求数据
        search_data = {
            'question': question,
            'dataset_ids': list(dataset_ids),
            'top_k': top_k
        }
        
        if document_ids:
            search_data['document_ids'] = [doc_id.strip() for doc_id in document_ids.split(',')]
        
        if similarity_threshold is not None:
            search_data['similarity_threshold'] = similarity_threshold
        
        if vector_similarity_weight is not None:
            search_data['vector_similarity_weight'] = vector_similarity_weight
        
        if highlight:
            search_data['highlight'] = highlight
        
        # 调用API
        response = client.post('/api/v1/retrieval', json_data=search_data)
        
        # 格式化输出
        if output_format == 'table':
            chunks = response.get('chunks', [])
            if chunks:
                # 简化显示，只显示关键信息
                simplified_chunks = []
                for chunk in chunks:
                    simplified_chunks.append({
                        'id': chunk.get('id', ''),
                        'dataset_id': chunk.get('dataset_id', ''),
                        'document_id': chunk.get('document_id', ''),
                        'similarity': f"{chunk.get('similarity', 0):.4f}",
                        'content_preview': chunk.get('content', '')[:100] + '...' if len(chunk.get('content', '')) > 100 else chunk.get('content', '')
                    })
                formatter.print_rich_table(simplified_chunks, f"检索结果 (共 {len(chunks)} 个块)")
            else:
                formatter.print_warning("未找到匹配的文档块")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"检索失败: {e}")


@retrieval.command()
@click.argument('question')
@click.argument('dataset_id')
@click.option('--top-k', type=int, default=5, help='返回的最大块数量')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def search_single_dataset(question, dataset_id, top_k, output_format):
    """在单个数据集中检索"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建请求数据
        search_data = {
            'question': question,
            'dataset_ids': [dataset_id],
            'top_k': top_k
        }
        
        # 调用API
        response = client.post('/api/v1/retrieval', json_data=search_data)
        
        # 格式化输出
        if output_format == 'table':
            chunks = response.get('chunks', [])
            if chunks:
                simplified_chunks = []
                for chunk in chunks:
                    simplified_chunks.append({
                        'id': chunk.get('id', ''),
                        'document_id': chunk.get('document_id', ''),
                        'similarity': f"{chunk.get('similarity', 0):.4f}",
                        'content_preview': chunk.get('content', '')[:150] + '...' if len(chunk.get('content', '')) > 150 else chunk.get('content', '')
                    })
                formatter.print_rich_table(simplified_chunks, f"数据集 {dataset_id} 检索结果")
            else:
                formatter.print_warning(f"在数据集 {dataset_id} 中未找到匹配的文档块")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"检索失败: {e}")


@retrieval.command()
@click.argument('question')
@click.argument('dataset_id')
@click.argument('document_id')
@click.option('--top-k', type=int, default=3, help='返回的最大块数量')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def search_single_document(question, dataset_id, document_id, top_k, output_format):
    """在单个文档中检索"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 构建请求数据
        search_data = {
            'question': question,
            'dataset_ids': [dataset_id],
            'document_ids': [document_id],
            'top_k': top_k
        }
        
        # 调用API
        response = client.post('/api/v1/retrieval', json_data=search_data)
        
        # 格式化输出
        if output_format == 'table':
            chunks = response.get('chunks', [])
            if chunks:
                simplified_chunks = []
                for chunk in chunks:
                    simplified_chunks.append({
                        'id': chunk.get('id', ''),
                        'similarity': f"{chunk.get('similarity', 0):.4f}",
                        'content': chunk.get('content', '')
                    })
                formatter.print_rich_table(simplified_chunks, f"文档 {document_id} 检索结果")
            else:
                formatter.print_warning(f"在文档 {document_id} 中未找到匹配的块")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"检索失败: {e}") 