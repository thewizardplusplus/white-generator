import enum
import pathlib

class Layout(enum.IntEnum):
  BASIC = 0
  RAQM = 1

class FreeTypeFont: ...

class ImageFont: ...

def truetype(
  font: pathlib.Path | None = None,
  size: int = 10,
  index: int = 0,
  encoding: str = '',
  layout_engine: Layout | None = None,
) -> FreeTypeFont: ...

def load_default(size: int | None = None) -> FreeTypeFont | ImageFont: ...
