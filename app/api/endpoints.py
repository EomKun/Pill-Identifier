from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.detection import DetectionService
from app.services.recognition import RecognitionService
import logging

router = APIRouter()

detection_service = DetectionService("app/models/best.pt")
recognization_service = RecognitionService(hf_token)

logger = logging.getLogger("uvicorn.error")

@router.post("/pills/analyzation")
async def analyze_pill(file: UploadFile = File(...)) :
    """알약 분석 엔드포인트

    Args:
        file(UploadFile): 요청에 포함된 파일(이미지)

    Returns:
        json 응답
    """
    crops_images = detection_service.detection_process(file)
    if not crops_image :
        logger.warning("탐지된 알약이 없습니다")
        return {"status": "success", "message": "탐지된 알약이 없습니다.", "pills": []}
    
    pill_names = await recognization_service.recognize_all(crops_images)

    # 식약처 API 연동 필요

    final_pills = []
    for i, res in enumerate(pill_names) :
        final_pills.append({
            "pill_index": i,
            "pill_name": res.get("label"),
            "confidence": res.get("score")
        })

    return {
        "status": "success",
        "total_detected": len(pill_names),
        "pills": final_pills
    }


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
