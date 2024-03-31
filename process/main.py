from typing import List
import numpy as np
from ultralytics import YOLO
import struct

from process.object_processing.object_processing_tools import ObjectTools
from process.object_processing.models import ObjectModelConfig
from process.communication_interface.serial_communication import SerialCommunication


class FrameProcessing:
    def __init__(self):
        self.execute = ObjectTools()

        # ball
        self.ball_detection_model: YOLO = YOLO(ObjectModelConfig.ball_model)
        self.ball_detection_classes: List[str] = ObjectModelConfig.ball_classes

        # communication
        self.communication = SerialCommunication()

    def process(self, image: np.ndarray) -> str:
        # Step 1: ball detect
        ball_bbox, ball_cls, ball_conf = self.execute.frame_model_inference(image, self.ball_detection_model,
                                                                            self.ball_detection_classes)
        # [axis x, axis z]
        error_vector = [0, 0]
        if len(ball_bbox) != 0:
            if ball_cls == 'blue ball':
                self.execute.draw_rect(image, ball_bbox, (255, 0, 0), 2)
                # x axis
                ball_xc, ball_yc = self.execute.extract_center_object(image, ball_bbox, (0, 0, 255), viz=True)
                frame_xc, frame_yc = self.execute.extract_center_frame(image)
                error_vector = self.execute.error_calculated_x_axis(ball_xc, frame_xc, error_vector)

                # z axis
                object_area = self.execute.calculate_area(ball_bbox)
                error_vector = self.execute.error_calculated_z_axis(object_area, error_vector)

                # send data
                vector_send = struct.pack("<ii", *error_vector)
                self.communication.sending_data(vector_send)

            elif ball_cls == 'green ball':
                self.execute.draw_rect(image, ball_bbox, (0, 255, 0), 2)

        else:
            vector_send = struct.pack("<ii", *error_vector)
            self.communication.sending_data(vector_send)
        print(f'vector send: {error_vector}')
        return ball_cls
