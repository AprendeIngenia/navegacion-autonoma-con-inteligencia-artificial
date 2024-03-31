import math
import cv2
import numpy as np
from typing import List, Tuple, Any


class ObjectTools:
    def __init__(self):
        pass

    def frame_model_inference(self, image: np.ndarray, model: Any, labels: List[str]) -> Tuple[List[int], str, float]:
        bbox = []
        cls = 0
        conf = 0

        results = model(image, stream=True, verbose=False, conf=0.7)

        for res in results:
            # Box
            boxes = res.boxes
            for box in boxes:
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Error < 0
                if x1 < 0: x1 = 0
                if y1 < 0: y1 = 0
                if x2 < 0: x2 = 0
                if y2 < 0: y2 = 0

                bbox = [x1, y1, x2, y2]

                # Class
                cls = int(box.cls[0])
                cls = labels[cls]

                # Confidence
                conf = math.ceil(box.conf[0])

        return bbox, cls, conf

    def draw_rect(self, image: np.ndarray, coordinates: List[int], color: Tuple[int, int, int],
                  thickness: int):
        xi, yi, xf, yf = coordinates
        cv2.rectangle(image, (xi, yi), (xf, yf), color, thickness)

    def extract_center_object(self, image: np.ndarray, coordinates: List[int], color: Tuple[int, int, int], viz: bool = True) -> Tuple[int, int]:
        xi, yi, xf, yf = coordinates
        xc, yc = int((xi + xf) / 2), int((yi + yf) / 2)
        if viz:
            cv2.circle(image, (xc, yc), 2, color, 2)
        return xc, yc

    def extract_center_frame(self, image: np.ndarray) -> Tuple[int, int]:
        al, an, c = image.shape
        xc_frame, xy_frame = int(an / 2), int(al / 2)
        return xc_frame, xy_frame

    def calculate_area(self, coordinates: List[int]):
        xi, yi, xf, yf = coordinates
        base = xf - xi
        altura = yf - yi
        area = base * altura
        return area

    def error_calculated_x_axis(self, xc_object: int, xc_frame: int, error_vector: List[int]) -> List[int]:
        error = xc_frame - xc_object
        error_abs = abs(error)
        if error_abs > 50:
            error_vector[0] = error
        else:
            error_vector[0] = 0
        return error_vector

    def error_calculated_z_axis(self, area_object: int, error_vector: List[int], area_set: int = 25500) -> List[int]:
        error = area_set - area_object
        error_abs = abs(error)
        if error_abs > 5000:
            error_vector[1] = error
        else:
            error_vector[1] = 0
        return error_vector


