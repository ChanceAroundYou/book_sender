import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseUploader(ABC):
    """基础上传器接口"""
    
    @abstractmethod
    def upload_file(self, file_path: str, key: Optional[str] = None) -> str:
        """上传文件到云存储
        
        Args:
            file_path: 本地文件路径
            key: 云存储中的文件键名，如果不指定则使用文件名
            
        Returns:
            str: 云存储中的文件键名
        """
        pass
    
    @abstractmethod
    def generate_url(self, key: str, expires_in: int = 604800) -> str:
        """生成预签名URL
        
        Args:
            key: 云存储中的文件键名
            expires_in: URL有效期（秒），默认7天
            
        Returns:
            str: 预签名URL
        """
        pass
    
    @abstractmethod
    def file_exists(self, key: str) -> bool:
        """检查文件是否存在
        
        Args:
            key: 云存储中的文件键名
            
        Returns:
            bool: 文件是否存在
        """
        pass
    
    @abstractmethod
    def get_file_info(self, key: str) -> Dict[str, Any]:
        """获取文件信息
        
        Args:
            key: 云存储中的文件键名
            
        Returns:
            Dict[str, Any]: 文件信息，包含大小、最后修改时间等
        """
        pass
    
    @abstractmethod
    def list_files(self, prefix: Optional[str] = None) -> List[Dict[str, Any]]:
        """列出文件
        
        Args:
            prefix: 文件前缀，用于过滤
            
        Returns:
            List[Dict[str, Any]]: 文件列表，每个文件包含键名、大小、最后修改时间等信息
        """
        pass
    
    @abstractmethod
    def delete_file(self, key: str) -> bool:
        """删除文件
        
        Args:
            key: 云存储中的文件键名
            
        Returns:
            bool: 是否删除成功
        """
        pass
    
    @abstractmethod
    def delete_files(self, keys: List[str]) -> Dict[str, bool]:
        """批量删除文件
        
        Args:
            keys: 云存储中的文件键名列表
            
        Returns:
            Dict[str, bool]: 每个文件的删除结果
        """
        pass

    def upload_and_get_url(self, file_path: str, 
                          key: Optional[str] = None,
                          expires_in: int = 604800) -> str:
        """上传文件并获取预签名URL
        
        Args:
            file_path: 本地文件路径
            key: 文件键名，如果不指定则使用文件名
            expires_in: URL有效期（秒），默认7天
            
        Returns:
            str: 预签名URL
        """
        key = self.upload_file(file_path, key)
        return self.generate_url(key, expires_in)
    
    def get_url(self, file_path: Optional[str] = None, key: Optional[str] = None, expires_in: int = 604800) -> str:
        if not key and not file_path:
            raise ValueError("key 和 file_path 不能同时为空")
        elif not key:
            key = os.path.basename(file_path)
        
        if not self.file_exists(key):
            if not file_path:
                raise FileNotFoundError(f"文件不存在: {key}, 请先提供文件路径以上传文件")
            else:
                self.upload_file(file_path, key)
        return self.generate_url(key, expires_in)
