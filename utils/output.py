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
        if not data:
            self.console.print("No data to display", style="yellow")
            return
        
        table = Table(title=title)
        
        # 添加列
        for key in data[0].keys():
            table.add_column(key, style="cyan")
        
        # 添加行
        for row in data:
            table.add_row(*[str(value) for value in row.values()])
        
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