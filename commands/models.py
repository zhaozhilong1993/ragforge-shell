import click
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def models():
    """Manage LLM models and configurations"""
    pass


@models.command()
@click.option('--format', 'output_format', default='table', type=click.Choice(['table', 'json']), help='Output format')
def list(output_format):
    """List all configured models"""
    try:
        client = APIClient()
        response = client.get('/v1/llm/my_llms')
        
        if isinstance(response, dict) and response.get('code') == 0:
            data = response.get('data', {})
            formatter = OutputFormatter(output_format)
            
            if output_format == 'table':
                # 格式化表格输出
                table_data = []
                for factory, config in data.items():
                    for llm in config.get('llm', []):
                        table_data.append({
                            'Factory': factory,
                            'Model Name': llm.get('name', ''),
                            'Type': llm.get('type', ''),
                            'Used Tokens': llm.get('used_token', 0)
                        })
                formatter.print_rich_table(table_data, "Configured Models")
            else:
                click.echo(formatter.format_output(data))
        else:
            click.echo(f"Error: {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@models.command()
@click.option('--type', 'model_type', required=True, 
              type=click.Choice(['chat', 'embedding', 'rerank', 'asr', 'image2text']), 
              help='Model type')
@click.option('--factory', required=True, help='LLM factory name')
@click.option('--name', required=True, help='Model name')
def set_default(model_type, factory, name):
    """Set default model for a specific type"""
    try:
        client = APIClient()
        
        payload = {
            'model_type': model_type,
            'llm_factory': factory,
            'llm_name': name
        }
        
        response = client.post('/v1/llm/set_default_model', json_data=payload)
        
        if isinstance(response, dict) and response.get('code') == 0:
            click.echo(f"✅ Default {model_type} model set to {name} in factory {factory}")
        else:
            click.echo(f"❌ Error: {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}")


@models.command()
@click.option('--factory', required=True, help='LLM factory name')
@click.option('--name', required=True, help='Model name')
@click.option('--type', 'model_type', required=True, help='Model type (chat, embedding, rerank, image2text)')
@click.option('--api-key', 'api_key', help='API key')
@click.option('--base-url', 'base_url', help='Base URL')
@click.option('--max-tokens', 'max_tokens', type=int, default=8192, help='Max tokens')
def add(factory, name, model_type, api_key, base_url, max_tokens):
    """Add a new model configuration"""
    try:
        client = APIClient()
        
        payload = {
            'llm_factory': factory,
            'llm_name': name,
            'model_type': model_type,
            'api_key': api_key or '',
            'api_base': base_url or '',
            'max_tokens': max_tokens
        }
        
        response = client.post('/v1/llm/add_llm', json_data=payload)
        
        if isinstance(response, dict) and response.get('code') == 0:
            click.echo("Model added successfully!")
        else:
            click.echo(f"Error: {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@models.command()
@click.option('--factory', required=True, help='LLM factory name')
@click.option('--name', required=True, help='Model name')
@click.option('--api-key', 'api_key', help='API key')
@click.option('--base-url', 'base_url', help='Base URL')
@click.option('--max-tokens', 'max_tokens', type=int, help='Max tokens')
def edit(factory, name, api_key, base_url, max_tokens):
    """Edit an existing model configuration"""
    try:
        client = APIClient()
        
        # 获取现有配置
        params = {
            'llm_factory': factory,
            'llm_name': name
        }
        response = client.get('/v1/llm/get_llm_config', params=params)
        
        if isinstance(response, dict) and response.get('code') == 0:
            current_config = response.get('data', {})
            
            # 更新配置
            payload = {
                'llm_factory': factory,
                'llm_name': name,
                'api_key': api_key if api_key is not None else current_config.get('api_key', ''),
                'api_base': base_url if base_url is not None else current_config.get('api_base', ''),
                'max_tokens': max_tokens if max_tokens is not None else current_config.get('max_tokens', 8192)
            }
            
            # 使用set_api_key来更新配置
            response = client.post('/v1/llm/set_api_key', json_data=payload)
            
            if isinstance(response, dict) and response.get('code') == 0:
                click.echo("Model configuration updated successfully!")
            else:
                click.echo(f"Error: {response.get('message', 'Unknown error')}")
        else:
            click.echo(f"Error: Model not found - {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@models.command()
@click.option('--factory', required=True, help='LLM factory name')
@click.option('--name', required=True, help='Model name')
def delete(factory, name):
    """Delete a model configuration"""
    try:
        client = APIClient()
        
        payload = {
            'llm_factory': factory,
            'llm_name': name
        }
        
        response = client.post('/v1/llm/delete_llm', json_data=payload)
        
        if isinstance(response, dict) and response.get('code') == 0:
            click.echo("Model deleted successfully!")
        else:
            click.echo(f"Error: {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@models.command()
@click.option('--factory', required=True, help='LLM factory name')
@click.option('--name', required=True, help='Model name')
def show(factory, name):
    """Show detailed configuration for a specific model"""
    try:
        client = APIClient()
        
        # 使用params参数而不是URL拼接
        params = {
            'llm_factory': factory,
            'llm_name': name
        }
        response = client.get('/v1/llm/get_llm_config', params=params)
        
        if isinstance(response, dict) and response.get('code') == 0:
            config = response.get('data', {})
            
            if config:
                click.echo(f"Model Configuration:")
                click.echo(f"  Factory: {config.get('llm_factory', '')}")
                click.echo(f"  Name: {config.get('llm_name', '')}")
                click.echo(f"  Type: {config.get('model_type', '')}")
                click.echo(f"  API Key: {'*' * 10 if config.get('api_key') else 'Not set'}")
                click.echo(f"  Base URL: {config.get('api_base', 'Not set')}")
                click.echo(f"  Max Tokens: {config.get('max_tokens', 8192)}")
                click.echo(f"  Used Tokens: {config.get('used_tokens', 0)}")
            else:
                click.echo("Model not found")
        else:
            click.echo(f"Error: {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}")


@models.command()
@click.option('--format', 'output_format', default='table', type=click.Choice(['table', 'json']), help='Output format')
def factories(output_format):
    """List available LLM factories"""
    try:
        client = APIClient()
        response = client.get('/v1/llm/factories')
        
        if isinstance(response, dict) and response.get('code') == 0:
            data = response.get('data', [])
            formatter = OutputFormatter(output_format)
            
            if output_format == 'table':
                table_data = []
                for factory in data:
                    table_data.append({
                        'Name': factory.get('name', ''),
                        'Tags': factory.get('tags', ''),
                        'Logo': factory.get('logo', '')
                    })
                formatter.print_rich_table(table_data, "Available LLM Factories")
            else:
                click.echo(formatter.format_output(data))
        else:
            click.echo(f"Error: {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}") 


@models.command()
@click.option('--format', 'output_format', default='table', type=click.Choice(['table', 'json']), help='Output format')
def default(output_format):
    """Show default model configuration"""
    try:
        client = APIClient()
        response = client.get('/v1/llm/default_models')
        
        if isinstance(response, dict) and response.get('code') == 0:
            data = response.get('data', {})
            formatter = OutputFormatter(output_format)
            
            if output_format == 'table':
                click.echo(f"Default Model Configuration:")
                click.echo(f"  Source: {data.get('source', 'unknown')}")
                click.echo()
                
                models = data.get('models', {})
                api_configs = data.get('api_configs', {})
                
                for model_type, model_id in models.items():
                    if model_id:  # 只显示有值的模型
                        click.echo(f"  {model_type}: {model_id}")
                        
                        # 显示API配置信息
                        if model_type in api_configs:
                            config = api_configs[model_type]
                            if config.get('api_base'):
                                click.echo(f"    API Base: {config['api_base']}")
                            if config.get('max_tokens'):
                                click.echo(f"    Max Tokens: {config['max_tokens']}")
                            if config.get('api_key'):
                                click.echo(f"    API Key: {config['api_key']}")
                        click.echo()
            else:
                click.echo(formatter.format_output(data))
        else:
            click.echo(f"Error: {response.get('message', 'Unknown error')}")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}") 