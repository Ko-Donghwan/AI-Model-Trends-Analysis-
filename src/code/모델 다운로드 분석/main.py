from model_analyzer import run_analysis

def main():
    """메인 실행 함수"""
    input_file = './csv/Model_2025-02-11-cumsum.csv'
    output_file = './csv/Model_2025-02-11_모델_순위.csv'
    tier_lengths, correlations = run_analysis(input_file, output_file)
    
    print("\n다운로드 기준별 모델 수:")
    for tier, count in tier_lengths.items():
        print(f"{tier}: {count}")
    
    print("\n순위 상관관계 분석 결과:")
    for pair, (corr, p_value) in correlations.items():
        print(f"{pair}: correlation={corr:.3f}, p-value={p_value:.3f}")

if __name__ == "__main__":
    main()