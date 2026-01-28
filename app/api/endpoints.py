# 비즈니스 로직 호출
# 엔드 포인트를 나눠야 할 필요가 있는지? 고민
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.detection import DetectionService

router = APIRouter()
detector = DetectionService("app/models/best.pt")

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