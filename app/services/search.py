from app.schemas.pill import PillDetailResponse, PillRecognitionResponse
from app.core.config import settings
import httpx, logging

logger = logging.getLogger("uvicorn.error")

class SearchService:
    def __init__(self) :
        self.data_api_url: str = settings.DATA_API_URL
        self.data_api_key: str = settings.PUBLIC_API_KEY

    async def get_enriched_pill_data(self, recognition_result: dict) -> PillRecognitionResponse:
        pill_name = recognition_result.get("label")
        confidence = recognition_result.get("score", 0.0)
        
        # 1. 하위 함수 호출 (예외 처리는 하위 함수가 전담)
        guide_info = await self.get_pill_detail(pill_name)
        
        # 2. 결과가 있을 때만 DTO 생성, 없으면 None 유지
        details = None
        if pill_name and pill_name != "unknown":
            if guide_info:
                details = PillDetailResponse(
                    effect=guide_info.get("efcyQesitm", "정보 없음"),
                    how_to_use=guide_info.get("useMethodQesitm", "정보 없음"),
                    caution=guide_info.get("atpnQesitm", "정보 없음"),
                    storage=guide_info.get("depositMethodQesitm", "정보 없음")
                )
            
        return PillRecognitionResponse(
            pill_index = 0,
            pill_name = pill_name, 
            confidence = confidence, 
            details = details
        )
    
    async def get_pill_detail(self, item_name: str):
        if not item_name or item_name == "unknown": 
            return None

        params = {
            "serviceKey": self.data_api_key,
            "itemName": item_name,
            "type": "json",
            "numOfRows": 1,
            "pageNo": 1
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(self.data_api_url, params=params)
                if response.is_error:
                    print(f"DEBUG: 식약처 서버 응답 내용 -> {response.text}") # 여기서 XML/JSON 형태의 상세 에러 확인 가능
                    response.raise_for_status()
                # response.raise_for_status() 
                
                data = response.json()
                items = data.get("body", {}).get("items", [])

                if items:
                    logger.info(f"조회 성공: {item_name}")
                    return items[0]
                
        except Exception as e:
            logger.error(f"식약처 API 오류 [{item_name}]: {type(e).__name__} - {str(e)}")
            
        return None