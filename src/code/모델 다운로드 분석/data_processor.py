import pandas as pd
from download_thresholds import DownloadThresholds

# 모든 기준값 리스트 생성
thresholds = [
    DownloadThresholds.VERY_HIGH,
    DownloadThresholds.HIGH,
    DownloadThresholds.MEDIUM,
    DownloadThresholds.LOW,
    DownloadThresholds.VERY_LOW,
    DownloadThresholds.MINIMAL
]

def calculate_changes(df: pd.DataFrame) -> pd.DataFrame:
    """일별 변화량 계산"""
    for day in range(1, 30):
        df[f"Change_{day+1}Day"] = df[f"{day+1}Day"] - df[f"{day}Day"]
        df[f"ChangeRate_{day+1}Day"] = (df[f"Change_{day+1}Day"] / df[f"{day}Day"]) * 100
    return df

def calculate_weighted_sum(df: pd.DataFrame, weights: dict) -> pd.DataFrame:
    """가중 평균 계산"""
    df['Change_2Day_to_30Day_WeightedSum'] = sum(
        df[col] * weight for col, weight in weights.items()
    ) / sum(weights.values())
    return df

# 일관성 점수 계산 함수
def calculate_consistency_score(row, threshold):
    """일관성 점수 계산: 임계값을 충족한 일수의 비율"""
    days_above_threshold = (row.loc['1Day':'30Day'] >= threshold).sum()
    total_days = 30  # 총 일수
    return (days_above_threshold / total_days) * 100

def calculate_cumulative_changes(df: pd.DataFrame) -> pd.DataFrame:
    """최근 30일간 누적 다운로드 계산"""
    for threshold in thresholds:
        # 누적 다운로드 계산
        df['Cumulative_Downloads'] = df.loc[:, '1Day':'30Day'].sum(axis=1)
        
        # 일관성 점수 계산
        df['Consistency_Score'] = df.apply(lambda row: calculate_consistency_score(row, threshold), axis=1)
    return df