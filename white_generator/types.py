import dataclasses
import pathlib

DEFAULT_IMAGE_WIDTH = 640
DEFAULT_IMAGE_HEIGHT = 480
DEFAULT_IMAGE_BACKGROUND_COLOR = '#ffffff'

DEFAULT_FONT_SIZE = 25
DEFAULT_FONT_COLOR = '#000000'

DEFAULT_RECTANGLE_LEFT = 0
DEFAULT_RECTANGLE_TOP = 0
DEFAULT_RECTANGLE_RIGHT = -1
DEFAULT_RECTANGLE_BOTTOM = -1

@dataclasses.dataclass
class ImageParameters:
    width: int = DEFAULT_IMAGE_WIDTH
    height: int = DEFAULT_IMAGE_HEIGHT
    background_color: str = DEFAULT_IMAGE_BACKGROUND_COLOR # TODO: make this a separate type
    background_image: pathlib.Path | None = None

@dataclasses.dataclass
class FontParameters:
    file: pathlib.Path
    size: int = DEFAULT_FONT_SIZE
    color: str = DEFAULT_FONT_COLOR # TODO: make this a separate type

@dataclasses.dataclass
class Rectangle:
    left: int = DEFAULT_RECTANGLE_LEFT
    top: int = DEFAULT_RECTANGLE_TOP
    right: int = DEFAULT_RECTANGLE_RIGHT
    bottom: int = DEFAULT_RECTANGLE_BOTTOM

class TextParameters:
    def __init__(self, options):
        self.font = FontParameters(
            file=options.font_file,
            size=options.font_size,
            color=options.font_color,
        )
        self.rectangle = Rectangle(
            left=options.text_left,
            top=options.text_top,
            right=options.text_right,
            bottom=options.text_bottom,
        )
        self.horizontal_align = options.text_horizontal_align
        self.vertical_align = options.text_vertical_align

class WatermarkParameters:
    def __init__(self, options):
        self.text = options.watermark_text
        self.size = options.watermark_size
        self.color = options.watermark_color
