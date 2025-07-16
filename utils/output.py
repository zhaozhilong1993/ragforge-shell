import json
import yaml
from typing import Dict, Any, List
from tabulate import tabulate
from rich.console import Console
from rich.table import Table


class OutputFormatter:
    """输出格式化工具"""
    
    def __init__(self, format_type: str = "table"):
        self.format_type = format_type
        self.console = Console()
    
    def format_output(self, data: Any, title: str = "") -> str:
        """格式化输出数据"""
        if self.format_type == "json":
            return self._format_json(data)
        elif self.format_type == "yaml":
            return self._format_yaml(data)
        elif self.format_type == "table":
            return self._format_table(data, title)
        else:
            return str(data)
    
    def _format_json(self, data: Any) -> str:
        """JSON格式输出"""
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _format_yaml(self, data: Any) -> str:
        """YAML格式输出"""
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
    
    def _format_table(self, data: Any, title: str = "") -> str:
        """表格格式输出"""
        if isinstance(data, dict):
            # 如果是字典，转换为键值对表格
            table_data = [[k, str(v)] for k, v in data.items()]
            headers = ["Key", "Value"]
        elif isinstance(data, list) and data and isinstance(data[0], dict):
            # 如果是字典列表，使用第一个字典的键作为表头
            headers = list(data[0].keys())
            table_data = [[row.get(h, "") for h in headers] for row in data]
        else:
            # 其他情况，直接转换为字符串
            return str(data)
        
        return tabulate(table_data, headers=headers, tablefmt="grid")
    
    def print_rich_table(self, data: List[Dict], title: str = ""):
        """使用Rich库打印彩色表格"""
        if not isinstance(data, list):
            data = []
        if not data:
            self.console.print("暂无数据", style="yellow")
            return
        
        table = Table(title=title, show_header=True, header_style="bold magenta")
        
        # 定义重要字段的显示优先级
        priority_fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'status']
        
        # 获取所有字段
        all_fields = set()
        for row in data:
            all_fields.update(row.keys())
        
        # 按优先级排序字段
        sorted_fields = []
        for field in priority_fields:
            if field in all_fields:
                sorted_fields.append(field)
                all_fields.remove(field)
        
        # 添加剩余字段
        sorted_fields.extend(sorted(all_fields))
        
        # 添加列，设置合适的宽度
        for field in sorted_fields:
            if field in ['id', 'status']:
                table.add_column(field, style="cyan", width=10)
            elif field in ['name']:
                table.add_column(field, style="green", width=20)
            elif field in ['description']:
                table.add_column(field, style="blue", width=30)
            elif field in ['created_at', 'updated_at']:
                table.add_column(field, style="yellow", width=20)
            else:
                table.add_column(field, style="white", width=15)
        
        # 添加行，处理长文本
        for row in data:
            row_values = []
            for field in sorted_fields:
                value = row.get(field, "")
                if isinstance(value, str) and len(value) > 25:
                    value = value[:22] + "..."
                elif isinstance(value, (dict, list)):
                    value = str(value)[:22] + "..." if len(str(value)) > 25 else str(value)
                row_values.append(str(value))
            table.add_row(*row_values)
        
        self.console.print(table)
    
    def print_success(self, message: str):
        """打印成功消息"""
        self.console.print(f"✅ {message}", style="green")
    
    def print_error(self, message: str):
        """打印错误消息"""
        self.console.print(f"❌ {message}", style="red")
    
    def print_warning(self, message: str):
        """打印警告消息"""
        self.console.print(f"⚠️  {message}", style="yellow")
    
    def print_info(self, message: str):
        """打印信息消息"""
        self.console.print(f"ℹ️  {message}", style="blue")
    
    def print_simple_list(self, data: List[Dict], title: str = ""):
        """简单列表显示（支持文档和数据集）"""
        if not isinstance(data, list):
            data = []
        if not data:
            self.console.print("暂无数据", style="yellow")
            return
        
        self.console.print(f"\n{title}", style="bold blue")
        self.console.print("=" * 50)
        
        for i, item in enumerate(data, 1):
            # 兼容文档和数据集
            doc_id = item.get('id', item.get('document_id', 'N/A'))
            name = item.get('name', 'N/A')
            description = item.get('description', '')
            created_at = item.get('created_at', item.get('create_time', 'N/A'))
            status = item.get('status', 'N/A')
            self.console.print(f"\n{i}. 文档ID: {doc_id}", style="cyan")
            self.console.print(f"   名称: {name}", style="green")
            if description:
                self.console.print(f"   描述: {description}", style="blue")
            self.console.print(f"   状态: {status}", style="yellow")
            self.console.print(f"   创建时间: {created_at}", style="white")
            self.console.print("-" * 30) 