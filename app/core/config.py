import os
from dotenv import load_dotenv

load_dotenv()

class Settings :
    HF_TOKEN: str = os.getenv("HUGGING_FACE_TOKEN")
    HUGGING_MODEL_URL: str = os.getenv("HUGGING_FACE_MODEL_URL")
    PUBLIC_API_KEY: str = os.getenv("PUBLIC_DATA_API_KEY")
    DATA_API_URL: str = os.getenv("DATA_API_URL")
    MODEL_PATH: str = os.getenv("YOLO_MODEL_PATH", "best.pt")
    SAVE_DIR: str = os.getenv("CROP_SAVE_DIR", "data/learning_dataset")

settings = Settings()