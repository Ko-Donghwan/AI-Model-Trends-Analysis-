from huggingface_downloader import HuggingFaceModelDownloader

if __name__ == "__main__":
    downloader = HuggingFaceModelDownloader("Model_2025-02-11_influence_top_10000.csv", "output.csv")
    downloader.fetch_and_save_models()
