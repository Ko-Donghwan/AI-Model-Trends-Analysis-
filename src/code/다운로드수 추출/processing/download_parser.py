import re
from typing import List, Tuple

class DownloadGraphParser:
    """다운로드 그래프 데이터를 처리하는 클래스"""

    @staticmethod
    def parse_path_data(path_data: str) -> List[Tuple[float, float]]:
        """SVG 경로 데이터를 좌표 리스트로 변환"""
        coordinates = re.findall(r'[-+]?[0-9]*\.?[0-9]+', path_data)
        return [(float(coordinates[i]), float(coordinates[i + 1])) 
                for i in range(0, len(coordinates), 2)]

    @staticmethod
    def normalize_downloads(points: List[Tuple[float, float]], 
                            total_downloads: int, 
                            num_days: int = 30) -> List[int]:
        """좌표 데이터를 정규화하여 일별 다운로드 수 계산 (음수 방지 적용)"""
        if not points:
            return [0] * num_days

        max_day = max(point[0] for point in points)
        scale_factor = num_days / max_day
        normalized_points = [(x * scale_factor, max(0, 100 - y)) for x, y in points]

        daily_downloads = [0] * num_days
        for i in range(len(normalized_points) - 1):
            DownloadGraphParser._interpolate_downloads(
                daily_downloads, normalized_points[i], normalized_points[i + 1])

        return DownloadGraphParser._scale_downloads(daily_downloads, total_downloads)

    @staticmethod
    def _interpolate_downloads(daily_downloads: List[int], 
                                point1: Tuple[float, float], 
                                point2: Tuple[float, float]) -> None:
        """두 좌표 사이의 다운로드 수를 선형 보간하여 채움 (음수 방지 적용)"""
        x1, y1 = point1
        x2, y2 = point2
        if x1 > x2:  # 좌표가 정렬되지 않았을 경우 정렬
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        
        for x in range(int(x1), int(x2) + 1):
            if x >= len(daily_downloads):
                break
            t = (x - x1) / (x2 - x1) if x2 != x1 else 0
            daily_downloads[x] = max(0, int(y1 + t * (y2 - y1)))  # 음수 방지

    @staticmethod
    def _scale_downloads(daily_downloads: List[int], total_downloads: int) -> List[int]:
        """총 다운로드 수에 맞게 일별 다운로드 수를 스케일 조정 (음수 방지 적용)"""
        sum_downloads = sum(daily_downloads)
        if sum_downloads == 0:
            return [0] * len(daily_downloads)
        
        scale_factor = total_downloads / sum_downloads
        return [max(0, int(round(d * scale_factor))) for d in daily_downloads]  # 음수 방지
