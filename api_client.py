import requests
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path


class APIClient:
    """API客户端封装类"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
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
            # 如果配置文件不存在，创建默认配置
            default_config = {
                'api': {
                    'base_url': 'http://localhost:9380',
                    'timeout': 30,
                    'headers': {}
                },
                'logging': {
                    'level': 'INFO',
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                }
            }
            self._save_config(default_config)
            return default_config
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件格式错误: {e}")
    
    def _save_config(self, config: Dict[str, Any]):
        """保存配置文件"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
    
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
            # Flask-Login期望直接的token，不是Bearer格式
            self.session.headers['Authorization'] = auth_token
    
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
    
    def get(self, endpoint: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """发送GET请求"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"GET {url}")
        
        try:
            # 对于GET请求，只设置Authorization头，不设置Content-Type
            request_headers = {}
            if 'Authorization' in self.session.headers:
                request_headers['Authorization'] = self.session.headers['Authorization']
            
            # 如果提供了自定义headers，则覆盖默认的
            if headers:
                request_headers.update(headers)
            
            # 使用requests.get而不是session.get，避免继承session的默认头
            response = requests.get(url, params=params, headers=request_headers, timeout=self.session.timeout)
            response.raise_for_status()
            return self._handle_response(response)
        except requests.exceptions.RequestException as e:
            self.logger.error(f"GET请求失败: {e}")
            raise
    
    def post(self, endpoint: str, data: Optional[Dict] = None, json_data: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict[str, Any]:
        """发送POST请求"""
        url = f"{self.base_url}{endpoint}"
        self.logger.info(f"POST {url}")
        
        try:
            response = self.session.post(url, data=data, json=json_data, files=files)
            response.raise_for_status()
            
            # 检查响应头中是否有Authorization
            auth_header = response.headers.get('Authorization')
            if auth_header:
                self.session.headers['Authorization'] = auth_header
                self.logger.info("从响应头获取认证令牌")
            
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
        """设置认证令牌并保存到配置文件"""
        # Flask-Login期望直接的token，不是Bearer格式
        self.session.headers['Authorization'] = token
        
        # 保存到配置文件
        if 'api' not in self.config:
            self.config['api'] = {}
        self.config['api']['auth_token'] = token
        self._save_config(self.config)
        
        self.logger.info("认证令牌已设置并保存")
    
    def clear_auth_token(self):
        """清除认证令牌并从配置文件删除"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        
        # 从配置文件删除
        if 'api' in self.config and 'auth_token' in self.config['api']:
            del self.config['api']['auth_token']
            self._save_config(self.config)
        
        self.logger.info("认证令牌已清除")
    
    def has_auth_token(self) -> bool:
        """检查是否有认证令牌"""
        return 'Authorization' in self.session.headers 