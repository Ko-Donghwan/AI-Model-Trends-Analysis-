from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ModelData:
    """모델 데이터를 저장하는 데이터 클래스"""
    name: str
    task: Optional[str]
    daily_downloads: List[int]
