import pandas as pd
from data_loader import load_data
from data_processor import calculate_changes, calculate_weighted_sum, calculate_cumulative_changes
from tier_manager import process_download_tiers
from correlation_calculator import calculate_correlations

def run_analysis(input_file: str, output_file: str):
    """전체 분석 실행"""
    df = load_data(input_file)
    df = calculate_changes(df)
    weights = {f'ChangeRate_{i}Day': i for i in range(2, 30)}
    df = calculate_weighted_sum(df, weights)
    df = calculate_cumulative_changes(df)
    
    tier_dfs, tier_lengths = process_download_tiers(df)
    merged_df = pd.concat(tier_dfs, ignore_index=True)
    
    merged_df['final_score'] = merged_df[['Cumulative_Downloads']].mean(axis=1)
    # 총 다운로드 수 
    merged_df.to_csv(output_file, index=False)

    merged_df['Growth_Rate_Rank'] = merged_df['Change_2Day_to_30Day_WeightedSum'].rank(ascending=False)
    # 다운로드 상승률
    merged_df['Consistency_Rank'] = merged_df['Consistency_Score'].rank(ascending=False)
    # 다운로드 일관성

    rank_data = {
        'Total_Downloads_Rank': merged_df['final_score'].rank(ascending=False).tolist(),
        'Growth_Rate_Rank': merged_df['Growth_Rate_Rank'].tolist(),
        'Consistency_Rank': merged_df['Consistency_Rank'].tolist()
    }
    rank_df = pd.DataFrame(rank_data)
    rank_df.to_csv("ranked_data.csv", index=False)  # CSV 저장
    correlations = calculate_correlations(rank_df)
    
    return tier_lengths, correlations