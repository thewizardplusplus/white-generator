import dataclasses
import pathlib

DEFAULT_IMAGE_WIDTH = 640
DEFAULT_IMAGE_HEIGHT = 480
DEFAULT_IMAGE_BACKGROUND_COLOR = '#ffffff'

@dataclasses.dataclass
class ImageParameters:
    width: int = DEFAULT_IMAGE_WIDTH
    height: int = DEFAULT_IMAGE_HEIGHT
    background_color: str = DEFAULT_IMAGE_BACKGROUND_COLOR # TODO: make this a separate type
    background_image: pathlib.Path | None = None

class FontParameters:
    def __init__(self, options):
        self.file = options.font_file
        self.size = options.font_size
        self.color = options.font_color

class Rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

class TextParameters:
    def __init__(self, options):
        self.font = FontParameters(options)
        self.rectangle = Rectangle(
            options.text_left,
            options.text_top,
            options.text_right,
            options.text_bottom,
        )
        self.horizontal_align = options.text_horizontal_align
        self.vertical_align = options.text_vertical_align

class WatermarkParameters:
    def __init__(self, options):
        self.text = options.watermark_text
        self.size = options.watermark_size
        self.color = options.watermark_color
