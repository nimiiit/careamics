from aenum import StrEnum


# TODO: custom?
# TODO: add all transforms from albumentations?
class SupportedTransform(StrEnum):
    """Transforms currently supported by CAREamics.
    """

    FLIP = "Flip"
    RANDOM_ROTATE90 = "RandomRotate90"
    NORMALIZE_WO_TARGET = "NormalizeWithoutTarget"
    MANIPULATE_N2V = "ManipulateN2V"
    # CUSTOM = "Custom"