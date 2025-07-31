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
@click.option('--force', is_flag=True, help='强制删除，不提示确认')
def delete(dataset_id, force):
    """删除数据集"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 如果不是强制删除，先确认
        if not force:
            confirm = click.confirm(f"确定要删除数据集 {dataset_id} 吗？此操作不可恢复。")
            if not confirm:
                formatter.print_info("取消删除操作")
                return
        
        # 先获取数据集信息
        try:
            response = client.get('/api/v1/datasets', headers={'Authorization': f"Bearer {api_token}"})
            datasets = response.get('data', [])
            dataset_name = "未知数据集"
            dataset_exists = False
            for dataset in datasets:
                if dataset.get('id') == dataset_id:
                    dataset_name = dataset.get('name', '未知数据集')
                    dataset_exists = True
                    break
        except:
            dataset_name = dataset_id
            dataset_exists = False
        
        if not dataset_exists:
            formatter.print_error(f"数据集 {dataset_id} 不存在")
            return
        
        # 尝试多种删除方法
        delete_success = False
        mark_deleted = False
        
        # 方法1: 直接DELETE请求
        try:
            client.delete(f'/api/v1/datasets/{dataset_id}', headers={'Authorization': f"Bearer {api_token}"})
            delete_success = True
            formatter.print_success(f"数据集 {dataset_name} ({dataset_id}) 删除成功")
        except Exception as e:
            formatter.print_warning(f"直接删除失败: {e}")
        
        # 方法2: 使用POST请求删除
        if not delete_success:
            try:
                client.post(f'/api/v1/datasets/{dataset_id}/delete', headers={'Authorization': f"Bearer {api_token}"})
                delete_success = True
                formatter.print_success(f"数据集 {dataset_name} ({dataset_id}) 删除成功")
            except Exception as e:
                formatter.print_warning(f"POST删除失败: {e}")
        
        # 方法3: 使用PUT请求标记删除
        if not delete_success:
            try:
                response = client.put(f'/api/v1/datasets/{dataset_id}', 
                                   json_data={'status': 'deleted'}, 
                                   headers={'Authorization': f"Bearer {api_token}"})
                mark_deleted = True
                formatter.print_warning(f"数据集 {dataset_name} ({dataset_id}) 已标记为删除状态")
                formatter.print_info("注意: 这只是标记删除，数据集可能仍然存在")
            except Exception as e:
                formatter.print_warning(f"标记删除失败: {e}")
        
        # 验证删除结果
        if delete_success or mark_deleted:
            try:
                # 等待一下再检查
                import time
                time.sleep(1)
                
                response = client.get('/api/v1/datasets', headers={'Authorization': f"Bearer {api_token}"})
                datasets = response.get('data', [])
                still_exists = False
                for dataset in datasets:
                    if dataset.get('id') == dataset_id:
                        still_exists = True
                        break
                
                if not still_exists:
                    formatter.print_success(f"✅ 数据集 {dataset_name} ({dataset_id}) 已成功删除")
                else:
                    if mark_deleted:
                        formatter.print_warning(f"⚠️  数据集 {dataset_name} ({dataset_id}) 已标记为删除，但可能仍存在于系统中")
                        formatter.print_info("建议通过Web界面手动删除")
                    else:
                        formatter.print_error(f"❌ 数据集 {dataset_name} ({dataset_id}) 删除失败")
            except Exception as e:
                formatter.print_warning(f"无法验证删除结果: {e}")
        else:
            formatter.print_error(f"❌ 删除数据集 {dataset_id} 失败")
            formatter.print_info("建议操作:")
            formatter.print_info("1. 通过Web界面手动删除")
            formatter.print_info("2. 或者使用其他删除方法")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"删除数据集失败: {e}")


@datasets.command()
@click.argument('dataset_id')
@click.option('--force', is_flag=True, help='强制删除，不提示确认')
def purge(dataset_id, force):
    """彻底删除数据集（通过重新创建的方式）"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 如果不是强制删除，先确认
        if not force:
            confirm = click.confirm(f"确定要彻底删除数据集 {dataset_id} 吗？此操作不可恢复，且会丢失所有数据。")
            if not confirm:
                formatter.print_info("取消删除操作")
                return
        
        # 先获取数据集信息
        try:
            response = client.get('/api/v1/datasets', headers={'Authorization': f"Bearer {api_token}"})
            datasets = response.get('data', [])
            dataset_name = "未知数据集"
            dataset_exists = False
            for dataset in datasets:
                if dataset.get('id') == dataset_id:
                    dataset_name = dataset.get('name', '未知数据集')
                    dataset_exists = True
                    break
        except:
            dataset_name = dataset_id
            dataset_exists = False
        
        if not dataset_exists:
            formatter.print_error(f"数据集 {dataset_id} 不存在")
            return
        
        formatter.print_info(f"开始彻底删除数据集: {dataset_name} ({dataset_id})")
        
        # 方法1: 尝试直接删除
        try:
            client.delete(f'/api/v1/datasets/{dataset_id}', headers={'Authorization': f"Bearer {api_token}"})
            formatter.print_success(f"✅ 数据集 {dataset_name} ({dataset_id}) 已成功删除")
            return
        except Exception as e:
            formatter.print_warning(f"直接删除失败: {e}")
        
        # 方法2: 尝试POST删除
        try:
            client.post(f'/api/v1/datasets/{dataset_id}/delete', headers={'Authorization': f"Bearer {api_token}"})
            formatter.print_success(f"✅ 数据集 {dataset_name} ({dataset_id}) 已成功删除")
            return
        except Exception as e:
            formatter.print_warning(f"POST删除失败: {e}")
        
        # 方法3: 尝试标记删除
        try:
            client.put(f'/api/v1/datasets/{dataset_id}', 
                      json_data={'status': 'deleted'}, 
                      headers={'Authorization': f"Bearer {api_token}"})
            formatter.print_warning(f"⚠️  数据集 {dataset_name} ({dataset_id}) 已标记为删除")
        except Exception as e:
            formatter.print_warning(f"标记删除失败: {e}")
        
        # 方法4: 通过Web界面删除的建议
        formatter.print_error(f"❌ 无法通过API删除数据集 {dataset_name} ({dataset_id})")
        formatter.print_info("建议操作:")
        formatter.print_info("1. 通过Web界面手动删除数据集")
        formatter.print_info("2. 或者联系管理员删除")
        formatter.print_info("3. 如果数据集不重要，可以忽略它")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"彻底删除数据集失败: {e}")


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


@datasets.command()
@click.argument('dataset_id')
@click.argument('embedding_model')
@click.option('--force', is_flag=True, help='强制更新，不提示确认')
def set_embedding_model(dataset_id, embedding_model, force):
    """设置数据集的embedding模型"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 如果不是强制更新，先确认
        if not force:
            confirm = click.confirm(f"确定要将数据集 {dataset_id} 的embedding模型更改为 {embedding_model} 吗？")
            if not confirm:
                formatter.print_info("取消更新操作")
                return
        
        # 先获取当前数据集信息
        try:
            response = client.get('/api/v1/datasets', headers={'Authorization': f"Bearer {api_token}"})
            datasets = response.get('data', [])
            current_embedding_model = "未知"
            dataset_name = "未知数据集"
            
            for dataset in datasets:
                if dataset.get('id') == dataset_id:
                    current_embedding_model = dataset.get('embedding_model', '未知')
                    dataset_name = dataset.get('name', '未知数据集')
                    break
            
            formatter.print_info(f"数据集: {dataset_name}")
            formatter.print_info(f"当前embedding模型: {current_embedding_model}")
            formatter.print_info(f"新embedding模型: {embedding_model}")
            
        except Exception as e:
            formatter.print_warning(f"获取数据集信息失败: {e}")
        
        # 构建更新数据
        update_data = {
            'embedding_model': embedding_model
        }
        
        # 尝试多种更新方法
        success = False
        
        # 方法1: 直接PUT请求
        try:
            response = client.put(f'/api/v1/datasets/{dataset_id}', 
                                json_data=update_data, 
                                headers={'Authorization': f"Bearer {api_token}"})
            success = True
        except Exception as e:
            formatter.print_warning(f"直接更新失败: {e}")
        
        # 方法2: 使用PATCH请求
        if not success:
            try:
                response = client.patch(f'/api/v1/datasets/{dataset_id}', 
                                      json_data=update_data, 
                                      headers={'Authorization': f"Bearer {api_token}"})
                success = True
            except Exception as e:
                formatter.print_warning(f"PATCH更新失败: {e}")
        
        # 方法3: 使用POST请求更新
        if not success:
            try:
                response = client.post(f'/api/v1/datasets/{dataset_id}/update', 
                                     json_data=update_data, 
                                     headers={'Authorization': f"Bearer {api_token}"})
                success = True
            except Exception as e:
                formatter.print_warning(f"POST更新失败: {e}")
        
        if success:
            formatter.print_success(f"数据集 {dataset_id} 的embedding模型已更新为 {embedding_model}")
        else:
            formatter.print_error(f"更新embedding模型失败，请通过Web界面手动更新")
            formatter.print_info("建议操作:")
            formatter.print_info("1. 删除当前数据集")
            formatter.print_info("2. 重新创建数据集（会自动使用默认embedding模型）")
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"设置embedding模型失败: {e}")


@datasets.command()
@click.argument('dataset_id')
def fix_embedding_model(dataset_id):
    """修复数据集的embedding模型（使用默认embedding模型）"""
    try:
        client = APIClient()
        formatter = OutputFormatter()
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 获取默认embedding模型
        try:
            response = client.get('/v1/llm/default_models', headers={'Authorization': f"Bearer {api_token}"})
            default_models = response
            default_embedding_model = None
            
            if isinstance(default_models, dict):
                embedding_config = default_models.get('embedding_model', '')
                if embedding_config:
                    # 提取模型名称
                    if '@' in embedding_config:
                        default_embedding_model = embedding_config.split('@')[0]
                    else:
                        default_embedding_model = embedding_config
            
            if not default_embedding_model:
                formatter.print_error("无法获取默认embedding模型")
                return
                
            formatter.print_info(f"默认embedding模型: {default_embedding_model}")
            
        except Exception as e:
            formatter.print_warning(f"获取默认embedding模型失败: {e}")
            # 使用常见的默认embedding模型
            default_embedding_model = "bge-m3___OpenAI-API"
        
        # 调用set_embedding_model命令
        set_embedding_model.callback(dataset_id, default_embedding_model, True)
        
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"修复embedding模型失败: {e}") 