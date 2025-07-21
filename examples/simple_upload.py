#!/usr/bin/env python3
"""
简单的文件上传示例

这个脚本演示了如何使用 RAGForge Shell 上传文件到数据集。
"""

import subprocess
import sys
import os


def run_command(cmd):
    """运行命令并显示结果"""
    print(f"执行: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout.strip():
                print(f"输出: {result.stdout.strip()}")
        else:
            print("❌ 失败")
            if result.stderr.strip():
                print(f"错误: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        return False


def main():
    """主函数"""
    print("🚀 RAGForge Shell 文件上传示例")
    print("=" * 50)
    
    # 检查参数
    if len(sys.argv) < 3:
        print("用法: python simple_upload.py <dataset_id> <file_path>")
        print("示例: python simple_upload.py 083591d662c911f08ba44a90b26523d1 test.txt")
        return
    
    dataset_id = sys.argv[1]
    file_path = sys.argv[2]
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    print(f"数据集ID: {dataset_id}")
    print(f"文件路径: {file_path}")
    print()
    
    # 1. 检查系统状态
    print("1. 检查系统状态...")
    run_command("uv run python main.py system status")
    print()
    
    # 2. 查看数据集信息
    print("2. 查看数据集信息...")
    run_command(f"uv run python main.py datasets show {dataset_id}")
    print()
    
    # 3. 查看上传前的文档列表
    print("3. 查看上传前的文档列表...")
    run_command(f"uv run python main.py documents list {dataset_id}")
    print()
    
    # 4. 上传文件
    print("4. 上传文件...")
    success = run_command(f"uv run python main.py documents upload {dataset_id} --file {file_path}")
    print()
    
    if success:
        # 5. 查看上传后的文档列表
        print("5. 查看上传后的文档列表...")
        run_command(f"uv run python main.py documents list {dataset_id}")
        print()
        
        # 6. 尝试检索文档内容
        print("6. 尝试检索文档内容...")
        run_command(f'uv run python main.py retrieval search "文档内容" {dataset_id}')
        print()
        
        print("🎉 文件上传完成！")
        print("\n💡 提示:")
        print("- 文档处理可能需要一些时间")
        print("- 可以使用 'documents list' 查看文档状态")
        print("- 可以使用 'retrieval search' 检索文档内容")
    else:
        print("❌ 文件上传失败")


if __name__ == "__main__":
    main() 