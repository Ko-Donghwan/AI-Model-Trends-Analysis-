from scraping.web_scraper import WebScraper
from scraping.model_parser import ModelParser
from processing.download_parser import DownloadGraphParser
from data.model_data import ModelData
from storage.csv_handler import CSVHandler

class HuggingFaceModelDownloader:
    """Hugging Face 모델 데이터를 수집하는 클래스"""

    def __init__(self, csv_file: str, output_file: str):
        self.scraper = WebScraper()
        self.csv_handler = CSVHandler(output_file)
        self.input_csv = CSVHandler(csv_file)  # 입력 CSV 파일 핸들러 추가
    
    def fetch_and_save_models(self) -> None:
        """CSV 파일에서 모델 ID를 읽어와 데이터를 수집 및 저장"""
        df = self.input_csv.load_data()  # CSV에서 데이터 불러오기
        if 'id' not in df.columns:
            raise KeyError("🚨 CSV 파일에 'id' 컬럼이 없습니다.")

        for model_id in df['id']:
            print(f"🔄 모델 수집 중: {model_id}")
            self.fetch_and_save_model(model_id)

    def fetch_and_save_model(self, model_name: str) -> None:
        """단일 모델 데이터 수집 및 저장"""
        url = f'https://huggingface.co/{model_name}'
        soup = self.scraper.get_page_content(url)
        task, total_downloads, path_data = ModelParser.extract_model_data(soup)

        daily_downloads = [0] * 30
        if path_data and total_downloads:
            points = DownloadGraphParser.parse_path_data(path_data)
            daily_downloads = DownloadGraphParser.normalize_downloads(points, int(total_downloads))

        model_data = ModelData(model_name, task, daily_downloads)
        self.csv_handler.save_model_data(model_data)
