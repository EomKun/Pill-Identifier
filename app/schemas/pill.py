from pydantic import BaseModel, Field
from typing import List, Optional

class PillDetailResponse(BaseModel) :
    """ 식약처 상세 정보 DTO
    """
    effect: str = Field(description = "효능", default = "정보 없음")
    how_to_use: str = Field(description = "복용법", default = "정보 없음")
    caution: str = Field(description = "주의사항", default = "정보 없음")
    storage: str = Field(description = "보관법", default = "정보 없음")

class PillRecognitionResponse(BaseModel) :
    """ 개별 알약 인식 결과 DTO
    """
    pill_index: int = Field(default = 0)
    pill_name: str = Field(default = "unknown", description = "제품명")
    confidence: float = Field(default = 0.0, ge = 0, le = 1, description = "신뢰도")
    details: Optional[PillDetailResponse] = None

class AnalazePillResponse(BaseModel) :
    """알약 분석 결과
    """
    status: str = "success"
    total_count: int
    pill_details: List[PillRecognitionResponse] = []