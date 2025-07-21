#!/usr/bin/env python3
"""
测试所有命令的脚本
"""

import subprocess
import sys
import time

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"测试: {description}")
    print(f"命令: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print("输出:")
        print(result.stdout)
        if result.stderr:
            print("错误:")
            print(result.stderr)
        print(f"返回码: {result.returncode}")
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("命令超时")
        return False
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False

def main():
    """主测试函数"""
    print("开始测试 RAGForge Shell 命令...")
    
    # 基础命令测试
    tests = [
        ("uv run python main.py --help", "显示帮助信息"),
        ("uv run python main.py version", "显示版本信息"),
        ("uv run python main.py config-show", "显示配置信息"),
        ("uv run python main.py api-list", "列出API端点"),
    ]
    
    # 系统命令测试
    system_tests = [
        ("uv run python main.py system --help", "系统命令帮助"),
        ("uv run python main.py system status", "系统状态"),
        ("uv run python main.py system version", "系统版本"),
        ("uv run python main.py system config", "系统配置"),
        ("uv run python main.py system interface-config", "接口配置"),
        ("uv run python main.py system token-list", "令牌列表"),
    ]
    
    # 用户命令测试
    user_tests = [
        ("uv run python main.py user --help", "用户命令帮助"),
        ("uv run python main.py user status", "用户状态"),
        ("uv run python main.py user info", "用户信息"),
        ("uv run python main.py user tenant-info", "租户信息"),
    ]
    
    # 数据集命令测试
    dataset_tests = [
        ("uv run python main.py datasets --help", "数据集命令帮助"),
        ("uv run python main.py datasets list", "数据集列表"),
    ]
    
    # 调试命令测试
    debug_tests = [
        ("uv run python main.py debug --help", "调试命令帮助"),
        ("uv run python main.py debug check-connection", "检查连接"),
    ]
    
    # 执行所有测试
    all_tests = tests + system_tests + user_tests + dataset_tests + debug_tests
    
    passed = 0
    failed = 0
    
    for cmd, desc in all_tests:
        if run_command(cmd, desc):
            passed += 1
        else:
            failed += 1
        time.sleep(1)  # 避免请求过于频繁
    
    print(f"\n{'='*60}")
    print("测试结果汇总:")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    print(f"总计: {passed + failed}")
    print(f"{'='*60}")
    
    if failed == 0:
        print("🎉 所有测试通过！")
        return 0
    else:
        print("⚠️  部分测试失败，请检查相关功能")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 