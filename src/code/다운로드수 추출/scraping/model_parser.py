import re
from bs4 import BeautifulSoup
from typing import Optional, Tuple

class ModelParser:
    """웹 페이지에서 모델 정보를 추출하는 클래스"""

    @staticmethod
    def extract_model_data(soup: BeautifulSoup) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """웹 페이지에서 모델의 태스크, 다운로드 수, 그래프 데이터 추출"""
        
        # 모델 태스크 추출
        task_element = soup.select_one('body > div > main > div.SVELTE_HYDRATER.contents > header > div > div.mb-3.flex.flex-wrap.md\:mb-4')
        task = None
        if task_element:
            task_link = task_element.find('a', href=re.compile(r'/models\?pipeline_tag=.*'))
            if task_link:
                task = task_link.text.strip()
                if task.lower() == 'transformers':
                    task = None

        # 총 다운로드 수 추출
        downloads_element = soup.select_one('body > div:nth-of-type(1) > main > div:nth-of-type(2) > section:nth-of-type(2) > div:nth-of-type(1) > dl > dd')
        total_downloads = downloads_element.text.replace(',', '') if downloads_element else None

        # 다운로드 그래프 데이터 추출
        graph_div = soup.select_one('html > body > div > main > div:nth-of-type(2) > section:nth-of-type(2) > div:nth-of-type(1) > div')
        path_data = graph_div.find('path').get('d') if graph_div and graph_div.find('path') else None

        return task, total_downloads, path_data
