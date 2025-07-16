import requests
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path


class APIClient:
    """API客户端封装类"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self._setup_session()
        self._setup_logging()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件 {config_path} 不存在")
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件格式错误: {e}")
    
    def _setup_session(self):
        """设置HTTP会话"""
        api_config = self.config.get('api', {})
        base_url = api_config.get('base_url', 'http://localhost:9380')
        timeout = api_config.get('timeout', 30)
        headers = api_config.get('headers', {})
        
        self.session.headers.update(headers)
        self.session.timeout = timeout
        self.base_url = base_url.rstrip('/')
        
        # 添加认证头（如果配置中有）
        auth_token = api_config.get('auth_token')
        if auth_token:
            self.session.headers['Authorization'] = f"Bearer {auth_token}"
    
    def _setup_logging(self):
        """设置日志"""
        log_config = self.config.get('logging', {})
        level = getattr(logging, log_config.get('level', 'INFO'))
        format_str = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        logging.basicConfig(level=level, format=format_str)
        self.logger = logging.getLogger(__name__)
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理API响应"""
        try:
            data = response.json()
            
            # 检查API错误码
            if isinstance(data, dict):
                code = data.get('code')
                message = data.get('message', '')
                
                if code == 100:  # 错误码
                    raise Exception(f"API错误: {message}")
                elif code == 401:  # 未认证
                    raise Exception(f"认证失败: {message}")
                elif code == 403:  # 权限不足
                    raise Exception(f"权限不足: {message}")
                elif code == 404:  # 资源不存在
                    raise Exception(f"资源不存在: {message}")
            
            return data
        except ValueError:
            # 如果不是JSON格式，返回文本内容
            return {"text": response.text}
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """发送GET请求"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"GET {url}")
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GET请求失败: {e}")
            raise
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送POST请求"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"POST {url}")
        
        try:
            response = self.session.post(url, data=data, json=json_data)
            response.raise_for_status()
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"POST请求失败: {e}")
            raise
    
    def put(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送PUT请求"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"PUT {url}")
        
        try:
            response = self.session.put(url, data=data, json=json_data)
            response.raise_for_status()
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"PUT请求失败: {e}")
            raise
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """发送DELETE请求"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"DELETE {url}")
        
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            return self._handle_response(response) if response.content else {}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"DELETE请求失败: {e}")
            raise
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置信息"""
        return self.config
    
    def set_auth_token(self, token: str):
        """设置认证令牌"""
        self.session.headers['Authorization'] = f"Bearer {token}"
        self.logger.info("认证令牌已设置")
    
    def clear_auth_token(self):
        """清除认证令牌"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        self.logger.info("认证令牌已清除") 