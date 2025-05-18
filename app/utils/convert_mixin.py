import json
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Iterable, List, Optional, Set
from uuid import UUID


class ConvertMixin:
    """可将对象及其嵌套属性转换为字典的 Mixin 类
    
    支持的类型：
    - 基本类型 (int, float, str, bool)
    - 容器类型 (dict, list, tuple, set)
    - 日期时间类型 (datetime, date, time)
    - 特殊类型 (Decimal, UUID, Enum)
    - 自定义对象 (实现了 to_dict 方法的对象)
    
    处理特性：
    - 递归转换嵌套结构
    - 处理循环引用
    - 优雅降级（对于不能转换的类型，尝试 str 转换）
    - 可自定义排除的属性
    """

    def _convert_value(
        self,
        value: Any,
        exclude: Set[str],
        max_depth: int,
        visited: Set[int],
        current_depth: int
    ) -> Any:
        """转换单个值为可序列化的格式"""
        if current_depth >= max_depth:
            return str(value)

        if value is None:
            return None

        obj_id = id(value)
        if obj_id in visited:
            return str(value)
        
        visited.add(obj_id)
        try:
            if isinstance(value, (int, float, str, bool)):
                return value

            if isinstance(value, (datetime, date, time)):
                return value.isoformat()

            if isinstance(value, (Decimal, UUID)):
                return str(value)

            if isinstance(value, Enum):
                return value.value

            if isinstance(value, dict):
                return self._convert_dict(
                    value,
                    exclude,
                    max_depth,
                    visited,
                    current_depth
                )
            
            if hasattr(value, '__dict__'):
                return self._convert_dict(
                    value.__dict__,
                    exclude,
                    max_depth,
                    visited,
                    current_depth
                )

            if isinstance(value, (list, tuple, set)):
                return self._convert_iterable(
                    value,
                    exclude,
                    max_depth,
                    visited,
                    current_depth
                )

            if hasattr(value, 'to_dict') and callable(value.to_dict):
                if isinstance(value, DictMixin):
                    return value.to_dict(
                        exclude=exclude,
                        max_depth=max_depth-current_depth
                    )
                return value.to_dict()
            
            if hasattr(value, 'to_iterable') and callable(value.to_iterable):
                if isinstance(value, InterableMixin):
                    return value.to_iterable(
                        exclude=exclude,
                        max_depth=max_depth-current_depth
                    )
                return value.to_iterable()

            return str(value)

        finally:
            visited.remove(obj_id)

    def _convert_dict(
        self,
        obj: Dict[str, Any],
        exclude: Set[str],
        max_depth: int,
        visited: Set[int],
        current_depth: int = 0
    ) -> Dict[str, Any]:
        """递归转换字典及其嵌套值
        
        Args:
            obj: 要转换的字典
            exclude: 要排除的键集合
            max_depth: 最大递归深度
            visited: 已访问对象的 id 集合（防止循环引用）
            current_depth: 当前递归深度
            
        Returns:
            转换后的字典
        """
        # 检查深度
        if current_depth >= max_depth:
            return str(obj)
        
        if not hasattr(obj, 'items'):
            return self._convert_value(
                obj,
                exclude,
                max_depth,
                visited,
                current_depth + 1
            )

        result = {}
        for key, value in obj.items():
            if key.startswith('_') or key in exclude:
                continue
            result[key] = self._convert_value(
                value,
                exclude,
                max_depth,
                visited,
                current_depth + 1
            )
        return result
    
    def _convert_iterable(
        self,
        obj: Iterable[Any],
        exclude: Set[str],
        max_depth: int,
        visited: Set[int],
        current_depth: int = 0
    ) -> Iterable[Any]:
        if current_depth >= max_depth:
            return [str(item) for item in obj]
        
        if not hasattr(obj, '__iter__'):
            return self._convert_value(
                obj,
                exclude,
                max_depth,
                visited,
                current_depth + 1
            )

        if isinstance(obj, list):
            return [
                self._convert_value(
                    item,
                    exclude,
                    max_depth,
                    visited,
                    current_depth + 1
                )
                for item in obj
            ]
        elif isinstance(obj, tuple):
            return tuple(
                self._convert_value(
                    item,
                    exclude,
                    max_depth,
                    visited,
                    current_depth + 1
                )
                for item in obj
            )
        elif isinstance(obj, set):
            return set(
                self._convert_value(
                    item,
                    exclude,
                    max_depth,
                    visited,
                    current_depth + 1
                )
                for item in obj
            )
        else:
            raise TypeError(f"Unsupported iterable type: {type(obj)}")

class DictMixin(ConvertMixin):
    def to_dict(
        self,
        obj: Any=None,
        exclude: Optional[Set[str]] = None,
        max_depth: int = 5
    ) -> Dict[str, Any]:
        """将对象转换为字典
        
        Args:
            exclude: 要排除的属性名集合
            max_depth: 最大递归深度，防止循环引用
            
        Returns:
            包含对象属性的字典
        """
        if obj is None:
            if self.__dict__:
                obj = self.__dict__
            else:
                return None

        return self._convert_dict(
            obj,
            exclude or set(),
            max_depth,
            visited=set(),
            current_depth=0
        )
    
class InterableMixin(ConvertMixin):
    def to_iterable(
        self,
        obj: Any=None,
        exclude: Optional[Set[str]] = None,
        max_depth: int = 5
    ) -> List[Any]:
        """将对象转换为列表
        
        Args:
            obj: 要转换的对象，默认为None
            exclude: 要排除的键集合
            max_depth: 最大递归深度
            
        Returns:
            转换后的列表
        """
        if obj is None:
            if hasattr(self, '__iter__'):
                obj = self
            else:
                return None

        return self._convert_iterable(
            obj,
            exclude or set(),
            max_depth,
            visited=set(),
            current_depth=0
        )
    
class JsonMixin(DictMixin, InterableMixin):
    def to_json(
        self,
        obj: Any=None,
        exclude: Optional[Set[str]] = None,
        max_depth: int = 5
    ) -> str:
        """将对象转换为JSON字符串
        
        Args:
            obj: 要转换的对象，默认为None
            exclude: 要排除的键集合
            max_depth: 最大递归深度
            
        Returns:
            JSON字符串
        """
        if obj is None:
            return 'null'
        if isinstance(obj, (list, tuple, set)):
            data = self.to_iterable(obj, exclude, max_depth)
        else:
            data = self.to_dict(obj, exclude, max_depth)
            
        return json.dumps(data)


def to_dict(obj, exclude: Optional[Set[str]] = None, max_depth: int = 5) -> Dict[str, Any]:
    return DictMixin().to_dict(obj, exclude, max_depth)

def to_iterable(obj, exclude: Optional[Set[str]] = None, max_depth: int = 5) -> Iterable[Any]:
    return InterableMixin().to_iterable(obj, exclude, max_depth)

def to_json(obj, exclude: Optional[Set[str]] = None, max_depth: int = 5) -> str:
    return JsonMixin().to_json(obj, exclude, max_depth)
