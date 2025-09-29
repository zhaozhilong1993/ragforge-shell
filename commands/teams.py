#!/usr/bin/env python3
"""
团队管理命令模块
提供团队相关的功能，包括查看可加入团队、加入团队、离开团队等
"""

import click
import yaml
from api_client import APIClient
from utils.output import OutputFormatter


@click.group()
def teams():
    """团队管理命令"""
    pass


@teams.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def list_available(output_format):
    """查看可加入的团队列表"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 调用API获取可加入的团队列表
        # 这里假设API端点为 /api/v1/teams/available
        response = client.get('/api/v1/teams/available', headers={'Authorization': f"Bearer {api_token}"})
        
        if response.get('code') != 0:
            formatter.print_error(f"获取团队列表失败: {response.get('message', '未知错误')}")
            return
        
        teams_data = response.get('data', [])
        
        if not teams_data:
            formatter.print_info("暂无可加入的团队")
            return
        
        # 格式化输出
        if output_format == 'table':
            # 准备表格数据
            table_data = []
            for team in teams_data:
                table_data.append({
                    'ID': team.get('id', ''),
                    '团队名称': team.get('name', ''),
                    '描述': team.get('description', ''),
                    '成员数量': team.get('member_count', 0),
                    '创建者': team.get('creator', ''),
                    '状态': team.get('status', ''),
                    '创建时间': team.get('create_time', ''),
                    '是否公开': '是' if team.get('is_public', False) else '否'
                })
            
            formatter.print_rich_table(table_data, "可加入的团队列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取团队列表失败: {e}")


@teams.command()
@click.argument('team_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def join(team_id, output_format):
    """加入指定团队"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 构建加入团队的请求数据
        join_data = {
            'team_id': team_id
        }
        
        # 调用API加入团队
        # 这里假设API端点为 /api/v1/teams/join
        response = client.post('/api/v1/teams/join', json_data=join_data, headers={'Authorization': f"Bearer {api_token}"})
        
        if response.get('code') == 0:
            formatter.print_success(f"成功加入团队 {team_id}")
        else:
            formatter.print_error(f"加入团队失败: {response.get('message', '未知错误')}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('data', {})], "加入团队结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"加入团队失败: {e}")


@teams.command()
@click.argument('team_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def leave(team_id, output_format):
    """离开指定团队"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 构建离开团队的请求数据
        leave_data = {
            'team_id': team_id
        }
        
        # 调用API离开团队
        # 这里假设API端点为 /api/v1/teams/leave
        response = client.post('/api/v1/teams/leave', json_data=leave_data, headers={'Authorization': f"Bearer {api_token}"})
        
        if response.get('code') == 0:
            formatter.print_success(f"成功离开团队 {team_id}")
        else:
            formatter.print_error(f"离开团队失败: {response.get('message', '未知错误')}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('data', {})], "离开团队结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"离开团队失败: {e}")


@teams.command()
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def my_teams(output_format):
    """查看我加入的团队列表"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 调用API获取我加入的团队列表
        # 这里假设API端点为 /api/v1/teams/my
        response = client.get('/api/v1/teams/my', headers={'Authorization': f"Bearer {api_token}"})
        
        if response.get('code') != 0:
            formatter.print_error(f"获取我的团队列表失败: {response.get('message', '未知错误')}")
            return
        
        teams_data = response.get('data', [])
        
        if not teams_data:
            formatter.print_info("您还没有加入任何团队")
            return
        
        # 格式化输出
        if output_format == 'table':
            # 准备表格数据
            table_data = []
            for team in teams_data:
                table_data.append({
                    'ID': team.get('id', ''),
                    '团队名称': team.get('name', ''),
                    '描述': team.get('description', ''),
                    '角色': team.get('role', ''),
                    '加入时间': team.get('join_time', ''),
                    '状态': team.get('status', '')
                })
            
            formatter.print_rich_table(table_data, "我的团队列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取我的团队列表失败: {e}")


@teams.command()
@click.argument('team_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def info(team_id, output_format):
    """查看团队详细信息"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 调用API获取团队详细信息
        # 这里假设API端点为 /api/v1/teams/{team_id}
        response = client.get(f'/api/v1/teams/{team_id}', headers={'Authorization': f"Bearer {api_token}"})
        
        if response.get('code') != 0:
            formatter.print_error(f"获取团队信息失败: {response.get('message', '未知错误')}")
            return
        
        team_data = response.get('data', {})
        
        # 格式化输出
        if output_format == 'table':
            # 准备详细信息表格
            info_data = [{
                '字段': '团队ID',
                '值': team_data.get('id', '')
            }, {
                '字段': '团队名称',
                '值': team_data.get('name', '')
            }, {
                '字段': '描述',
                '值': team_data.get('description', '')
            }, {
                '字段': '成员数量',
                '值': team_data.get('member_count', 0)
            }, {
                '字段': '创建者',
                '值': team_data.get('creator', '')
            }, {
                '字段': '创建时间',
                '值': team_data.get('create_time', '')
            }, {
                '字段': '是否公开',
                '值': '是' if team_data.get('is_public', False) else '否'
            }, {
                '字段': '状态',
                '值': team_data.get('status', '')
            }]
            
            formatter.print_rich_table(info_data, f"团队 {team_id} 详细信息")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取团队信息失败: {e}")


@teams.command()
@click.argument('team_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def members(team_id, output_format):
    """查看团队成员列表"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 调用API获取团队成员列表
        # 这里假设API端点为 /api/v1/teams/{team_id}/members
        response = client.get(f'/api/v1/teams/{team_id}/members', headers={'Authorization': f"Bearer {api_token}"})
        
        if response.get('code') != 0:
            formatter.print_error(f"获取团队成员列表失败: {response.get('message', '未知错误')}")
            return
        
        members_data = response.get('data', [])
        
        if not members_data:
            formatter.print_info("该团队暂无成员")
            return
        
        # 格式化输出
        if output_format == 'table':
            # 准备成员表格数据
            table_data = []
            for member in members_data:
                table_data.append({
                    '用户ID': member.get('user_id', ''),
                    '用户名': member.get('username', ''),
                    '昵称': member.get('nickname', ''),
                    '角色': member.get('role', ''),
                    '加入时间': member.get('join_time', ''),
                    '状态': member.get('status', '')
                })
            
            formatter.print_rich_table(table_data, f"团队 {team_id} 成员列表")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"获取团队成员列表失败: {e}")


@teams.command()
@click.argument('name')
@click.option('--description', help='团队描述')
@click.option('--is_public', is_flag=True, help='是否公开团队')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def create(name, description, is_public, output_format):
    """创建新团队"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 构建创建团队的请求数据
        team_data = {
            'name': name,
            'is_public': is_public
        }
        
        if description:
            team_data['description'] = description
        
        # 调用API创建团队
        # 这里假设API端点为 /api/v1/teams
        response = client.post('/api/v1/teams', json_data=team_data, headers={'Authorization': f"Bearer {api_token}"})
        
        if response.get('code') == 0:
            formatter.print_success(f"团队 {name} 创建成功")
        else:
            formatter.print_error(f"创建团队失败: {response.get('message', '未知错误')}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('data', {})], "创建团队结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"创建团队失败: {e}")


@teams.command()
@click.argument('team_id')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'yaml']), 
              help='输出格式')
def delete(team_id, output_format):
    """删除团队（仅团队创建者可操作）"""
    try:
        client = APIClient()
        formatter = OutputFormatter(output_format)
        
        # 检查是否有API token
        api_token = client.config.get('api', {}).get('api_token')
        if not api_token:
            formatter.print_error("未找到API令牌，请先登录")
            return
        
        # 调用API删除团队
        # 这里假设API端点为 /api/v1/teams/{team_id}
        response = client.delete(f'/api/v1/teams/{team_id}', headers={'Authorization': f"Bearer {api_token}"})
        
        if response.get('code') == 0:
            formatter.print_success(f"团队 {team_id} 删除成功")
        else:
            formatter.print_error(f"删除团队失败: {response.get('message', '未知错误')}")
            return
        
        # 格式化输出
        if output_format == 'table':
            formatter.print_rich_table([response.get('data', {})], "删除团队结果")
        else:
            print(formatter.format_output(response))
            
    except Exception as e:
        formatter = OutputFormatter()
        formatter.print_error(f"删除团队失败: {e}")
