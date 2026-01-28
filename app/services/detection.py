# YOLO 모델 기반 추론 및 이미지 크롭
from ultralytics import YOLO
from PIL import Image
import io

class DetectionService :
    """
    YOLO 모델 기반 알약 객체 탐지 서비스
    """
    def __init__(self, model_path: str) :
        self.model = YOLO(model_path)

    def _get_detections(self, image: Image.Image, conf: float = 0.5) :
        """모델 기반으로 탐지된 알약의 좌표 리스트를 반환(내부 호출 용)

        Args:
            image (Image.Image): 입력된 PIL 이미지 객체
            conf (float): 탐지 신뢰도 임계값. 이 수치보다 확신이 높은 객체만 포함. (Defaults = 0.5)

        Returns:
            list: 탐지된 알약들의 좌표 정보 [[x1, y1, x2, y2], ...] 리스트.
        """
        results = self.model.predict(image, conf = conf)

        return [box.xyxy[0].toList() for r in results for box in r.boxes]
    
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
        image = Image.open(io.BytesIO(image_bytes))

        boxes = self.get_detections(image)
        crops = self.crop_detections(image, boxes)

        return crops