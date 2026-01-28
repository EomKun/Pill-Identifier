# 💊 Pill-Detection & Medication Guide System
> 다중 알약 식별 및 공공 데이터 결합형 비동기 복약 가이드 생성 시스템

이 프로젝트는 단일 이미지 내 여러 알약을 탐지(Detection)하고, 각 객체를 병렬로 식별(Classification)한 뒤, 공공 데이터 API와 결합하여 사용자에게 구조화된 복약 정보를 제공하는 백엔드 시스템입니다.

## 🎯 Key Engineering Focus
- 비동기 병렬 추론 (Parallel Inference): asyncio와 httpx를 사용하여 다수의 알약 식별 요청을 Hugging Face API에 병렬로 전송, 전체 응답 시간을 단일 처리 대비 획기적으로 단축.

- 이미지 프로세싱 파이프라인: 직접 학습한 YOLOv11n 모델로 추출된 Bounding Box 좌표를 기반으로 Pillow를 활용한 실시간 이미지 크롭 및 전처리 로직 구현.

- 외부 API 통합 (Data Enrichment): 식약처 공공 API와의 통신을 통해 식별된 약물 ID에 맞는 효능, 주의사항 등의 데이터를 동적으로 매칭.

- 환경 격리 및 최적화: uv를 통한 엄격한 의존성 관리 및 환경에 최적화된 PyTorch 빌드 구성.

## 🏗️ System Architecture
> [!TODO]
다 만들고 이미지와 아키텍처 그려서 삽입
1. Image Ingestion: 사용자가 FastAPI 엔드포인트를 통해 알약 사진 업로드.

2. Object Detection: YOLOv11n 모델이 이미지 내 알약 개수와 위치(X, Y, W, H) 파악.

3. Dynamic Cropping: 파이썬 로직이 탐지된 좌표를 바탕으로 이미지를 개별 알약 단위로 분할.

4. Concurrent Classification: 분할된 각 이미지를 Swin Transformer 모델에 비동기적으로 전달하여 약물명 식별.

5. Information Merging: 식별된 약물명을 키값으로 공공 데이터베이스의 복약 가이드 정보 결합.

6. Structured Response: 모든 정보가 결합된 최종 JSON 데이터 반환.

## 🛠️ Tech Stack

- Framework: FastAPI

- Package Manager: uv

- Concurrency: asyncio, httpx

- Environment: Python 3.12+

- AI & ML Pipeline
  - Object Detection: YOLOv11n
    - Training Dataset: [Pill_detection](https://universe.roboflow.com/mohamed-attia-e2mor/pill-detection-llp4r)

  - Image Classification: -

  - Image Processing: Pillow (PIL)

  - Runtime: PyTorch (CUDA 12.4 Optimized for RTX 4070)

## 🚀 Quick Start
1. Requirements
   - NVIDIA Driver 설치
   - uv (Fast Python package installer)

2. Installation & Run
   
    ```bash
    # 1. 저장소 클론
    git clone https://github.com/your-id/pill-detection-system.git
    cd pill-detection-system

    # 2. 의존성 설치 및 가상환경 구성 (uv.lock 기반)
    uv sync

    # 3. 서버 실행
    uv run uvicorn main:app --reload
    ```

## 🔌 API Specification (현재는 예시)
`POST /api/v1/analyze`
- 이미지를 분석하여 알약 정보와 복약 가이드를 생성합니다.

#### Response Body

```json
{
  "request_id": "uuid-1234-5678",
  "detected_count": 2,
  "results": [
    {
      "pill_name": "타이레놀정500mg",
      "confidence": 0.992,
      "info": {
        "effect": "감기로 인한 발열 및 통증, 두통, 신경통",
        "dosage": "1회 1~2정씩 빈속을 피해 복용",
        "precaution": "음주 후 복용 시 간 손상 유발 가능"
      }
    }
  ]
}
```

## 📂 Project Structure

```text
pill-identifier/
├── app/
│   ├── main.py              # FastAPI 실행 및 엔드포인트 정의
│   ├── core/                # 설정 및 공통 로직
│   │   └── config.py        # 모델 경로, API 키 관리
│   ├── api/                 # API 라우터 (V1, V2 등)
│   │   └── endpoints.py     # 비즈니스 로직 호출
│   ├── services/            # 핵심 로직 (AI 추론, 이미지 처리)
│   │   ├── detection.py     # YOLO 모델 추론 및 크롭
│   │   └── recognition.py   # 식약처 API 또는 식별 모델 연동
│   ├── models/              # 가중치 파일 저장
│   │   └── best.pt          # 학습된 YOLOv11 모델
│   └── utils/               # 유틸리티 (이미지 변환 등)
│       └── helpers.py
├── data/                    # (선택) 임시 저장 폴더
│   └── temp_crops/
├── requirements.txt         # 종속성 관리
├── .env                     # 환경 변수 (API KEY 등)
├── .python-version          # 프로젝트 파이썬 버전
├── pyproject.toml           # 프로젝트 의존성 및 설정
└───uv.lock                  # 의존성 잠금 파일
```