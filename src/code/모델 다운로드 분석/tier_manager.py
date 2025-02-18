import pandas as pd
from download_thresholds import DownloadThresholds

def create_download_tier_df(df: pd.DataFrame, threshold: int, excluded_indices=None) -> pd.DataFrame:
    """다운로드 기준별 데이터프레임 생성"""
    days_columns = [f"{i+1}Day" for i in range(30)]
    filtered_df = df[df[days_columns].ge(threshold).all(axis=1)]
    if excluded_indices is not None:
        filtered_df = filtered_df[~filtered_df.index.isin(excluded_indices)]
    return filtered_df.sort_values(by='Cumulative_Downloads', ascending=False)

def process_download_tiers(df: pd.DataFrame) -> tuple:
    """다운로드 기준별 데이터 처리"""
    thresholds = DownloadThresholds()
    excluded_indices = set()
    tier_dfs = []
    tier_lengths = {}
    
    for threshold, name in [
        (thresholds.VERY_HIGH, 'very_high'),
        (thresholds.HIGH, 'high'),
        (thresholds.MEDIUM, 'medium'),
        (thresholds.LOW, 'low'),
        (thresholds.VERY_LOW, 'very_low'),
        (thresholds.MINIMAL, 'minimal')
    ]:
        tier_df = create_download_tier_df(df, threshold, excluded_indices)
        print(len(tier_df))
        tier_dfs.append(tier_df)
        tier_lengths[name] = len(tier_df)
        excluded_indices.update(tier_df.index)
    
    return tier_dfs, tier_lengths