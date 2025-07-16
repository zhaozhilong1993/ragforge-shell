#!/usr/bin/env python3
"""
RAGForge API 使用示例
展示如何使用API客户端进行各种操作
"""

from api_client import APIClient
from utils.output import OutputFormatter


def example_datasets_operations():
    """数据集操作示例"""
    print("=== 数据集操作示例 ===")
    
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 1. 列出所有数据集
        print("\n1. 列出所有数据集:")
        response = client.get('/api/v1/datasets')
        formatter.print_rich_table(response.get('datasets', []), "数据集列表")
        
    except Exception as e:
        formatter.print_error(f"数据集操作失败: {e}")


def example_documents_operations():
    """文档操作示例"""
    print("\n=== 文档操作示例 ===")
    
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 假设有一个数据集ID
        dataset_id = "example_dataset_id"
        
        # 1. 列出数据集中的所有文档
        print(f"\n1. 列出数据集 {dataset_id} 中的所有文档:")
        response = client.get(f'/api/v1/datasets/{dataset_id}/documents')
        formatter.print_rich_table(response.get('documents', []), f"数据集 {dataset_id} 的文档列表")
        
    except Exception as e:
        formatter.print_error(f"文档操作失败: {e}")


def example_retrieval_operations():
    """检索操作示例"""
    print("\n=== 检索操作示例 ===")
    
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 检索示例
        search_data = {
            'question': '什么是机器学习？',
            'dataset_ids': ['example_dataset_id'],
            'top_k': 5
        }
        
        print("\n1. 执行检索:")
        response = client.post('/api/v1/retrieval', json_data=search_data)
        
        chunks = response.get('chunks', [])
        if chunks:
            simplified_chunks = []
            for chunk in chunks:
                simplified_chunks.append({
                    'id': chunk.get('id', ''),
                    'dataset_id': chunk.get('dataset_id', ''),
                    'document_id': chunk.get('document_id', ''),
                    'similarity': f"{chunk.get('similarity', 0):.4f}",
                    'content_preview': chunk.get('content', '')[:100] + '...' if len(chunk.get('content', '')) > 100 else chunk.get('content', '')
                })
            formatter.print_rich_table(simplified_chunks, "检索结果")
        else:
            formatter.print_warning("未找到匹配的文档块")
        
    except Exception as e:
        formatter.print_error(f"检索操作失败: {e}")


def example_create_dataset():
    """创建数据集示例"""
    print("\n=== 创建数据集示例 ===")
    
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 创建数据集数据
        dataset_data = {
            'dataset': {
                'name': '示例数据集',
                'description': '这是一个示例数据集'
            }
        }
        
        print("创建数据集...")
        response = client.post('/api/v1/datasets', json_data=dataset_data)
        
        formatter.print_success("数据集创建成功")
        formatter.print_rich_table([response.get('dataset', {})], "创建的数据集")
        
    except Exception as e:
        formatter.print_error(f"创建数据集失败: {e}")


def example_create_document():
    """创建文档示例"""
    print("\n=== 创建文档示例 ===")
    
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 假设有一个数据集ID
        dataset_id = "example_dataset_id"
        
        # 创建文档数据
        document_data = {
            'document': {
                'name': '示例文档',
                'content': '这是文档的内容，包含一些关于机器学习的知识。'
            }
        }
        
        print(f"在数据集 {dataset_id} 中创建文档...")
        response = client.post(f'/api/v1/datasets/{dataset_id}/documents', json_data=document_data)
        
        formatter.print_success("文档创建成功")
        formatter.print_rich_table([response.get('document', {})], "创建的文档")
        
    except Exception as e:
        formatter.print_error(f"创建文档失败: {e}")


def example_api_documentation():
    """获取API文档示例"""
    print("\n=== API文档示例 ===")
    
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 获取API文档
        response = client.get('/apispec.json')
        
        print("API端点:")
        if isinstance(response, dict) and 'paths' in response:
            for path, methods in response['paths'].items():
                for method, info in methods.items():
                    print(f"  {method.upper()} {path} - {info.get('summary', '')}")
        
    except Exception as e:
        formatter.print_error(f"获取API文档失败: {e}")


def main():
    """主函数"""
    print("RAGForge API 使用示例")
    print("=" * 50)
    
    # 运行各种示例
    example_datasets_operations()
    example_documents_operations()
    example_retrieval_operations()
    example_create_dataset()
    example_create_document()
    example_api_documentation()
    
    print("\n示例执行完成!")


if __name__ == '__main__':
    main() 