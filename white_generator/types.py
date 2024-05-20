import dataclasses
import pathlib
import enum

DEFAULT_IMAGE_WIDTH = 640
DEFAULT_IMAGE_HEIGHT = 480
DEFAULT_IMAGE_BACKGROUND_COLOR = '#ffffff'

DEFAULT_FONT_SIZE = 25
DEFAULT_FONT_COLOR = '#000000'

DEFAULT_RECTANGLE_LEFT = 0
DEFAULT_RECTANGLE_TOP = 0
DEFAULT_RECTANGLE_RIGHT = -1
DEFAULT_RECTANGLE_BOTTOM = -1

DEFAULT_TEXT_VERTICAL_ALIGN = 'center'

DEFAULT_WATERMARK_SIZE = 12
DEFAULT_WATERMARK_COLOR = '#808080'

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

# TODO: replace with `enum.StrEnum` after upgrading to Python 3.11
class HorizontalAlign(str, enum.Enum):
    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'

DEFAULT_TEXT_HORIZONTAL_ALIGN = HorizontalAlign.CENTER

@dataclasses.dataclass
class TextParameters:
    font: FontParameters
    rectangle: Rectangle = dataclasses.field(default_factory=Rectangle)
    horizontal_align: HorizontalAlign = DEFAULT_TEXT_HORIZONTAL_ALIGN
    vertical_align: str = DEFAULT_TEXT_VERTICAL_ALIGN # TODO: make this a separate type

@dataclasses.dataclass
class WatermarkParameters:
    text: str = ''
    size: int = DEFAULT_WATERMARK_SIZE
    color: str = DEFAULT_WATERMARK_COLOR # TODO: make this a separate type
