# 식별 모델
# 식약처 API 도는 식별 모델 등으로 연동 예정
import asyncio
import httpx
from PIL import Image
from app.core.config import settings
import io

class RecognitionService:
    """
    인식 모델 기반 알약 식별 서비스
    """
    def __init__(self):
        # Hugging Face API 설정
        self.api_url = settings.HUGGING_MODEL_URL
        self.headers = {"Authorization": f"Bearer {settings.HF_TOKEN}"}

    async def _classify_one(self, client: httpx.AsyncClient, image_bytes: bytes):
        """개별 알약 식별요청(내부용)
        
        Args: 
            client(httpx.AsyncClient): 
            image_bytes(bytes): 

        return:

        """
        try:
            response = await client.post(
                self.api_url,
                headers = self.headers,
                content = image_bytes,
                timeout = 10.0
            )

            return response.json()[0] if response.status_code == 200 else {"label": "unknown"}
        except Exception as e :
            return {"error": str(e)}

    async def recognize_all(self, pill_images: list[Image.Image]):
        """모든 검출된 알약 이미지들을 병렬 식별 요청
        
        Args: 
            pill_images(list[Image.Image]): 식별된 알약 이미지 리스트

        Returns:
            results: 검출된 이미지의 알약 명 리스트
        """
        async with httpx.AsyncClient() as client :
            tasks = []
            for img in pill_images :
                buf = io.BytesIO()
                img.save(buf, format = 'JPEG')
                tasks.append(self._classify_one(client, buf.getvalue()))

            results = await asyncio.gather(*tasks)
            return results