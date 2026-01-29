from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.detection import DetectionService
from app.services.recognition import RecognitionService
from app.services.search import SearchService
from app.schemas.pill import AnalazePillResponse
import asyncio, logging

router = APIRouter()

detection_service = DetectionService()
recognization_service = RecognitionService()
search_service = SearchService()

logger = logging.getLogger("uvicorn.error")

@router.post("/pills/analyzation", response_model = AnalazePillResponse)
async def analyze_pill(file: UploadFile = File(...)) :
    """알약 분석 엔드포인트

    Args:
        file(UploadFile): 요청에 포함된 파일(이미지)

    Returns:
        json 응답
    """
    image_bytes = await file.read()
    crops_images = detection_service.detection_process(image_bytes)
    if not crops_images :
        logger.warning("탐지된 알약이 없습니다")
        return AnalazePillResponse(status="success", total_count=0, pills=[])
    
    recognition_results = await recognization_service.recognize_all(crops_images)

    tasks = [search_service.get_enriched_pill_data(res) for res in recognition_results]
    final_pills = await asyncio.gather(*tasks)

    return AnalazePillResponse(
        status = "success",
        total_count = len(final_pills),
        pill_details = final_pills
    )



@router.post("/pills/detect")
async def detect_pills(file: UploadFile = File(...)):
    """객체 탐지 확인용 임시 엔드포인트

    Args:
        file(UploadFile): 요청에 포함된 파일(이미지)

    Returns:
        json 응답 (status, pill_count, message)
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="이미지 파일만 업로드 가능합니다.")

    try:
        # 이미지 바이트 읽기
        image_bytes = await file.read()

        saved_pill_paths = detector.detection_process(image_bytes)

        # 현재는 크롭된 이미지 객체 리스트이므로, 개수와 간단한 메시지만 반환
        return {
            "count": len(saved_pill_paths),
            "pill_locations": saved_pill_paths  # ["data/temp_crops/2024..._0.jpg", ...]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")
