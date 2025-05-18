from typing import Type, TypeVar

from app.distributor.base import BaseDistributor
from app.distributor.ses_distributor import SESDistributor
from app.distributor.smtp_distributor import SMTPDistributor

T = TypeVar('T', bound=BaseDistributor) 

def create_distributor(distributor_type: str, *args, **kwargs) -> T:
    """创建分发器实例
    
    Args:
        distributor_type: 分发器类型，支持 'smtp' 和 'ses'
        
    Returns:
        BaseDistributor: 分发器实例
    """
    distributor_map: dict[str, Type[T]] = {
        'smtp': SMTPDistributor,
        'ses': SESDistributor,
    }

    if distributor_type not in distributor_map:
        raise ValueError(f"Unsupported distributor type: {distributor_type}")

    return distributor_map.get(distributor_type)(*args, **kwargs)
