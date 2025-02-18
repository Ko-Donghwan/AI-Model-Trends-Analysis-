import pandas as pd

def load_data(input_file: str) -> pd.DataFrame:
    """CSV 파일을 로드하는 함수"""
    return pd.read_csv(input_file)