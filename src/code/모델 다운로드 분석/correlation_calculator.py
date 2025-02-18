import pandas as pd
import scipy.stats as stats

def calculate_correlations(df: pd.DataFrame) -> dict:
    """순위 상관관계 계산"""
    rank_cols = ['Total_Downloads_Rank', 'Growth_Rate_Rank', 'Consistency_Rank']
    correlations = {}
    
    for i in range(len(rank_cols)):
        for j in range(i + 1, len(rank_cols)):
            col1, col2 = rank_cols[i], rank_cols[j]
            corr, p_value = stats.spearmanr(df[col1], df[col2])
            correlations[f"{col1}_{col2}"] = (corr, p_value)
    
    return correlations