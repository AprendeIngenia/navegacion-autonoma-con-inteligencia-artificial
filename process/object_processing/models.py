from pydantic import BaseModel
from typing import List

from process.object_processing.object_models.ball_model_detect import (ball_detection_model, ball_detection_classes)


class ObjectModels(BaseModel):
    # ball model
    ball_model: str = ball_detection_model
    ball_classes: List[str] = ball_detection_classes

    # another models


ObjectModelConfig = ObjectModels()