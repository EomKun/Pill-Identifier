# YOLO 모델 기반 추론 및 이미지 크롭
from ultralytics import YOLO
from PIL import Image
from datetime import datetime
import io, os, logging

logger = logging.getLogger("uvicorn.error")

class DetectionService :
    """
    YOLO 모델 기반 알약 객체 탐지 서비스
    """

    def __init__(self, model_path: str, base_save_dir: str = "data/learning_dataset") :
        try:
            self.model = YOLO(model_path)
            logger.info(f"모델 로드 완료: {model_path}")
            
            self.base_save_dir = base_save_dir
            self.origin_dir = os.path.join(base_save_dir, "originals")
            self.crop_dir = os.path.join(base_save_dir, "crops")

            for path in [self.origin_dir, self.crop_dir] :
                if not os.path.exists(path) :
                    os.makedirs(path)

        except Exception as e:
            logger.error(f"모델 로드 실패: {str(e)}")
            raise e
        
    def _get_detections(self, image: Image.Image, conf: float = 0.45) :
        """모델 기반으로 탐지된 알약의 좌표 리스트를 반환(내부 호출 용)

        Args:
            image (Image.Image): 입력된 PIL 이미지 객체
            conf (float): 탐지 신뢰도 임계값. 이 수치보다 확신이 높은 객체만 포함. (Defaults = 0.5)

        Returns:
            list: 탐지된 알약들의 좌표 정보 [[x1, y1, x2, y2], ...] 리스트.
        """
        results = self.model.predict(image, conf = conf)

        return [box.xyxy[0].tolist() for r in results for box in r.boxes]
    
    def _crop_detections(self, image: Image.Image, boxes: list) :
        """입력된 좌표들을 바탕으로 이미지를 크롭(내부 호출 용)

        Args:
            image (Image.Image): 입력된 PIL 이미지 객체
            boxes (list): 탐지된 객체 좌표 리스트
        
        Returns:
            list: 크롭 된 이미지 리스트
        """
        return [image.crop(box) for box in boxes]
    
    def detection_process(self, image_bytes: bytes) :
        """객체 탐지 및 학습용 데이터 자동 저장

        Args: 
            image_bytes(bytes): 바이트화 된 이미지
        
        Returns:
            crops(list): 인식 서비스로 넘길 크롭된 이미지 객체 리스트
        """
        try : 
            image = Image.open(io.BytesIO(image_bytes))
            request_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            logger.info("이미지 수신 완료")

            boxes = self._get_detections(image)
            crops = self._crop_detections(image, boxes)
            logger.info(f"ID: {request_id} | {len(boxes)}개 객체 탐지 및 저장 시작")

            for i, crop in enumerate(crops):
                crop_file_name = f"{request_id}_crop_{i}.jpg"
                crop.save(os.path.join(self.crop_dir, crop_file_name), "JPEG")

            return crops
        
        except Exception as e :
            logger.error("객체 탐지 중 오류 발생", exc_info=True)
            raise e