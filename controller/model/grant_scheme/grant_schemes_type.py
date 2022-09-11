from enum import Enum


class GrantSchemeType(Enum):
    STUDENT_ENCOURAGEMENT_BONUS = "student encouragement bonus"
    MULTIGENERATION_SCHEME = "multigeneration scheme"
    ELDER_BONUS = "elder bonus"
    BABY_SUNSHINE_GRANT = "baby sunshine grant"
    YOLO_GST_GRANT = "yolo gst grant"

    @staticmethod
    def is_valid(scheme):
        schemes = [s.value for s in GrantSchemeType]
        return scheme in schemes