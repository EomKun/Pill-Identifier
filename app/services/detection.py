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

    def __init__(self, model_path: str, save_dir: str = "data/temp_crops") :
        try:
            self.model = YOLO(model_path)
            logger.info(f"모델 로드 완료: {model_path}")
            self.save_dir = save_dir

            # 저장 폴더가 없으면 생성
            if not os.path.exists(self.save_dir):
                os.makedirs(self.save_dir)
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
        """객체 탐지 프로세싱

        Args: 
            image_bytes: 
        
        Returns:
            crops(list): 
        """
        try : 
            image = Image.open(io.BytesIO(image_bytes))
            logger.info("이미지 수신 완료")

            boxes = self._get_detections(image)
            crops = self._crop_detections(image, boxes)
            logger.info(f"탐지 결과 {len(boxes)}의 객체 발견")

            """
            해당 부분은 나중에 삭제 예정
            """
            saved_paths = []
            request_id = datetime.now().strftime("%Y%m%d_%H%M%S")

            for i, crop in enumerate(crops):
                # 파일명 형식: 20240522_1430_0.jpg
                file_name = f"{request_id}_{i}.jpg"
                file_path = os.path.join(self.save_dir, file_name)
                
                # 실제 파일 저장
                crop.save(file_path, "JPEG")
                saved_paths.append(file_path)

            # return crops
            return saved_paths
        
        except Exception as e :
            logger.error("객체 탐지 중 오류 발생", exc_info=True)
            raise e