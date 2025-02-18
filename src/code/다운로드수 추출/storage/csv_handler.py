import pandas as pd
from pathlib import Path
from data.model_data import ModelData

class CSVHandler:
    """CSV 데이터를 관리하는 클래스"""

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def save_model_data(self, model_data: ModelData) -> None:
        """모델 데이터를 CSV 파일에 저장"""
        data = {
            "Model_name": [model_data.name],
            "Model_task": [model_data.task],
            **{f"{i+1}Day": [model_data.daily_downloads[i]] 
               for i in range(len(model_data.daily_downloads))}
        }
        df = pd.DataFrame(data)
        
        if self.file_path.exists():
            existing_df = pd.read_csv(self.file_path)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_csv(self.file_path, index=False)

    def load_data(self) -> pd.DataFrame:
        """CSV 파일에서 데이터를 불러와 DataFrame으로 반환"""
        if self.file_path.exists():
            return pd.read_csv(self.file_path)
        else:
            raise FileNotFoundError(f"🚨 {self.file_path} 파일이 존재하지 않습니다.")