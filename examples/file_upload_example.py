#!/usr/bin/env python3
"""
RAGForge Shell 文件上传使用示例

这个脚本演示了如何使用 RAGForge Shell 进行完整的文件上传和管理流程。
"""

import subprocess
import time
import json
import os
from pathlib import Path


def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'='*60}")
    print(f"执行: {description}")
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
        return result.returncode == 0, result.stdout
    except subprocess.TimeoutExpired:
        print("命令超时")
        return False, ""
    except Exception as e:
        print(f"执行命令时出错: {e}")
        return False, ""


def create_test_file():
    """创建测试文件"""
    test_content = """这是一个测试文档

用于演示 RAGForge Shell 的文件上传功能。

文档内容：
- 这是第一段内容
- 这是第二段内容  
- 这是第三段内容

测试要点：
1. 文件上传功能是否正常
2. API调用是否成功
3. 错误处理是否完善
4. 输出格式是否正确

技术细节：
- 使用Bearer格式的API token进行认证
- 支持多种文件格式（PDF、DOC、TXT等）
- 自动处理文件编码
- 提供详细的错误信息

这个文档将被上传到测试数据集中，用于验证整个工作流程。
"""
    
    test_file = "test_upload_document.txt"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print(f"✅ 创建测试文件: {test_file}")
    return test_file


def main():
    """主函数 - 演示完整的文件上传流程"""
    print("🚀 开始 RAGForge Shell 文件上传演示")
    
    # 1. 检查系统状态
    success, _ = run_command(
        "uv run python main.py system status",
        "检查系统状态"
    )
    if not success:
        print("❌ 系统状态检查失败，退出演示")
        return
    
    # 2. 查看数据集列表
    success, output = run_command(
        "uv run python main.py datasets list --format json",
        "查看数据集列表"
    )
    if not success:
        print("❌ 获取数据集列表失败，退出演示")
        return
    
    # 解析数据集ID
    try:
        data = json.loads(output)
        datasets = data.get('data', [])
        if not datasets:
            print("❌ 没有找到数据集，请先创建数据集")
            return
        
        dataset_id = datasets[0]['id']
        dataset_name = datasets[0]['name']
        print(f"✅ 使用数据集: {dataset_name} (ID: {dataset_id})")
    except Exception as e:
        print(f"❌ 解析数据集信息失败: {e}")
        return
    
    # 3. 查看数据集中的文档（上传前）
    print(f"\n📋 上传前的文档列表:")
    run_command(
        f"uv run python main.py documents list {dataset_id}",
        f"查看数据集 {dataset_name} 的文档列表"
    )
    
    # 4. 创建测试文件
    test_file = create_test_file()
    
    # 5. 上传文件
    success, _ = run_command(
        f"uv run python main.py documents upload {dataset_id} --file {test_file}",
        f"上传文件 {test_file} 到数据集 {dataset_name}"
    )
    if not success:
        print("❌ 文件上传失败")
        return
    
    # 6. 查看上传后的文档列表
    print(f"\n📋 上传后的文档列表:")
    run_command(
        f"uv run python main.py documents list {dataset_id}",
        f"查看数据集 {dataset_name} 的文档列表"
    )
    
    # 7. 查看文档详细信息
    success, output = run_command(
        f"uv run python main.py documents list {dataset_id} --format json",
        f"获取文档详细信息"
    )
    
    if success:
        try:
            data = json.loads(output)
            docs = data.get('data', {}).get('docs', [])
            if docs:
                latest_doc = docs[0]  # 最新的文档
                doc_id = latest_doc['id']
                doc_name = latest_doc['name']
                
                print(f"\n📄 查看文档详情: {doc_name}")
                run_command(
                    f"uv run python main.py documents show {dataset_id} {doc_id}",
                    f"查看文档 {doc_name} 的详细信息"
                )
                
                # 8. 等待文档处理（可选）
                print(f"\n⏳ 等待文档处理...")
                print("注意: 文档处理可能需要一些时间，这取决于文档大小和系统负载")
                
                # 9. 尝试检索文档内容
                print(f"\n🔍 尝试检索文档内容:")
                run_command(
                    f'uv run python main.py retrieval search "测试文档" {dataset_id}',
                    f"在数据集 {dataset_name} 中检索 '测试文档'"
                )
                
        except Exception as e:
            print(f"❌ 解析文档信息失败: {e}")
    
    # 10. 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"✅ 清理测试文件: {test_file}")
    
    print(f"\n{'='*60}")
    print("🎉 文件上传演示完成！")
    print(f"{'='*60}")
    print("\n📝 演示总结:")
    print("✅ 系统状态检查")
    print("✅ 数据集列表获取")
    print("✅ 文件上传")
    print("✅ 文档列表查看")
    print("✅ 文档详情查看")
    print("✅ 文档检索测试")
    print("\n💡 使用提示:")
    print("- 使用 'uv run python main.py documents upload <dataset_id> --file <file_path>' 上传文件")
    print("- 使用 'uv run python main.py documents list <dataset_id>' 查看文档列表")
    print("- 使用 'uv run python main.py retrieval search <query> <dataset_id>' 检索文档")
    print("- 支持多种文件格式: PDF、DOC、DOCX、TXT、MD 等")


if __name__ == "__main__":
    main() 