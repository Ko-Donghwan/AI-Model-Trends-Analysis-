from dataclasses import dataclass

@dataclass
class DownloadThresholds:
    """다운로드 수 기준값 정의"""
    VERY_HIGH = 10000
    HIGH = 1000
    MEDIUM = 100
    LOW = 50
    VERY_LOW = 10
    MINIMAL = 0