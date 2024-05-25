import unittest
import unittest.mock

from PIL import ImageDraw
from PIL import ImageFont

from . import text
from . import types

class TestFitText(unittest.TestCase):
  def setUp(self) -> None:
    self.image_draw = unittest.mock.create_autospec(ImageDraw.ImageDraw)
    self.font = ImageFont.load_default()

  def test_empty(self) -> None:
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, '', text_parameters, self.font)

    self.assertEqual(fitted_text, '')
    self.assertEqual(self.image_draw.multiline_textbbox.call_count, 0)

  def test_only_spaces(self) -> None:
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, '  ', text_parameters, self.font)

    self.assertEqual(fitted_text, '  ')
    self.assertEqual(self.image_draw.multiline_textbbox.call_count, 0)

  def test_single_line_without_wrapping(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [
      (0, None, 10, None),
      (0, None, 20, None),
      (0, None, 30, None),
    ]

    text_line = 'single line without wrapping'
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, text_line, text_parameters, self.font)

    self.assertEqual(fitted_text, 'single line without wrapping')
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'single line', self.font),
      unittest.mock.call((0, 0), 'single line without', self.font),
      unittest.mock.call((0, 0), 'single line without wrapping', self.font),
    ])

  def test_single_line_with_wrapping(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [
      (0, None, 90, None),
      (0, None, 110, None),
      (0, None, 90, None),
    ]

    text_line = 'single line with wrapping'
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, text_line, text_parameters, self.font)

    self.assertEqual(fitted_text, 'single line\nwith wrapping')
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'single line', self.font),
      unittest.mock.call((0, 0), 'single line with', self.font),
      unittest.mock.call((0, 0), 'single line\nwith wrapping', self.font),
    ])

  def test_single_line_with_wrapping_on_word_boundary(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [
      (0, None, 100, None),
      (0, None, 110, None),
      (0, None, 100, None),
    ]

    text_line = 'single line with wrapping'
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, text_line, text_parameters, self.font)

    self.assertEqual(fitted_text, 'single line\nwith wrapping')
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'single line', self.font),
      unittest.mock.call((0, 0), 'single line with', self.font),
      unittest.mock.call((0, 0), 'single line\nwith wrapping', self.font),
    ])

  def test_single_line_with_wrapping_and_extra_spaces(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [
      (0, None, 90, None),
      (0, None, 110, None),
      (0, None, 90, None),
    ]

    text_line = '  single  line  with  wrapping  '
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, text_line, text_parameters, self.font)

    self.assertEqual(fitted_text, 'single line\nwith wrapping')
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'single line', self.font),
      unittest.mock.call((0, 0), 'single line with', self.font),
      unittest.mock.call((0, 0), 'single line\nwith wrapping', self.font),
    ])

  def test_multiple_lines_without_wrapping(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [
      (0, None, 10, None),
      (0, None, 20, None),
      (0, None, 30, None),
      (0, None, 10, None),
      (0, None, 20, None),
      (0, None, 30, None),
    ]

    text_lines = 'line #1: multiple lines\nline #2: without wrapping'
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, text_lines, text_parameters, self.font)

    self.assertEqual(fitted_text, 'line #1: multiple lines\nline #2: without wrapping')
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'line #1:', self.font),
      unittest.mock.call((0, 0), 'line #1: multiple', self.font),
      unittest.mock.call((0, 0), 'line #1: multiple lines', self.font),
      unittest.mock.call((0, 0), 'line #2:', self.font),
      unittest.mock.call((0, 0), 'line #2: without', self.font),
      unittest.mock.call((0, 0), 'line #2: without wrapping', self.font),
    ])

  def test_multiple_lines_with_wrapping(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [
      (0, None, 90, None),
      (0, None, 110, None),
      (0, None, 90, None),
      (0, None, 90, None),
      (0, None, 110, None),
      (0, None, 90, None),
    ]

    text_lines = 'line #1: multiple lines\nline #2: with wrapping'
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, text_lines, text_parameters, self.font)

    self.assertEqual(fitted_text, 'line #1:\nmultiple lines\nline #2:\nwith wrapping')
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'line #1:', self.font),
      unittest.mock.call((0, 0), 'line #1: multiple', self.font),
      unittest.mock.call((0, 0), 'line #1:\nmultiple lines', self.font),
      unittest.mock.call((0, 0), 'line #2:', self.font),
      unittest.mock.call((0, 0), 'line #2: with', self.font),
      unittest.mock.call((0, 0), 'line #2:\nwith wrapping', self.font),
    ])

  def test_multiple_lines_with_wrapping_on_word_boundary(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [
      (0, None, 100, None),
      (0, None, 110, None),
      (0, None, 100, None),
      (0, None, 100, None),
      (0, None, 110, None),
      (0, None, 100, None),
    ]

    text_lines = 'line #1: multiple lines\nline #2: with wrapping'
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, text_lines, text_parameters, self.font)

    self.assertEqual(fitted_text, 'line #1:\nmultiple lines\nline #2:\nwith wrapping')
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'line #1:', self.font),
      unittest.mock.call((0, 0), 'line #1: multiple', self.font),
      unittest.mock.call((0, 0), 'line #1:\nmultiple lines', self.font),
      unittest.mock.call((0, 0), 'line #2:', self.font),
      unittest.mock.call((0, 0), 'line #2: with', self.font),
      unittest.mock.call((0, 0), 'line #2:\nwith wrapping', self.font),
    ])

  def test_multiple_lines_with_wrapping_and_extra_spaces(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [
      (0, None, 90, None),
      (0, None, 110, None),
      (0, None, 90, None),
      (0, None, 90, None),
      (0, None, 110, None),
      (0, None, 90, None),
    ]

    text_lines = '  line  #1:  multiple  lines  \n  line  #2:  with  wrapping  '
    text_parameters = types.TextParameters(rectangle=types.Rectangle(left=50, right=150))
    fitted_text = text.fit_text(self.image_draw, text_lines, text_parameters, self.font)

    self.assertEqual(fitted_text, 'line #1:\nmultiple lines\nline #2:\nwith wrapping')
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'line #1:', self.font),
      unittest.mock.call((0, 0), 'line #1: multiple', self.font),
      unittest.mock.call((0, 0), 'line #1:\nmultiple lines', self.font),
      unittest.mock.call((0, 0), 'line #2:', self.font),
      unittest.mock.call((0, 0), 'line #2: with', self.font),
      unittest.mock.call((0, 0), 'line #2:\nwith wrapping', self.font),
    ])

class TestGetTextPosition(unittest.TestCase):
  def setUp(self) -> None:
    self.image_draw = unittest.mock.create_autospec(ImageDraw.ImageDraw)
    self.font = ImageFont.load_default()

  def test_left_top(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.LEFT,
      vertical_align=types.VerticalAlign.TOP,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 40)
    self.assertEqual(text_top, 60)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

  def test_center_top(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.CENTER,
      vertical_align=types.VerticalAlign.TOP,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 65)
    self.assertEqual(text_top, 60)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

  def test_right_top(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.RIGHT,
      vertical_align=types.VerticalAlign.TOP,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 90)
    self.assertEqual(text_top, 60)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

  def test_left_center(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.LEFT,
      vertical_align=types.VerticalAlign.CENTER,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 40)
    self.assertEqual(text_top, 72)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

  def test_center_center(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.CENTER,
      vertical_align=types.VerticalAlign.CENTER,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 65)
    self.assertEqual(text_top, 72)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

  def test_right_center(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.RIGHT,
      vertical_align=types.VerticalAlign.CENTER,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 90)
    self.assertEqual(text_top, 72)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

  def test_left_bottom(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.LEFT,
      vertical_align=types.VerticalAlign.BOTTOM,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 40)
    self.assertEqual(text_top, 85)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

  def test_center_bottom(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.CENTER,
      vertical_align=types.VerticalAlign.BOTTOM,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 65)
    self.assertEqual(text_top, 85)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

  def test_right_bottom(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 150, 75)]

    text_parameters = types.TextParameters(
      rectangle=types.Rectangle(left=40, top=60, right=240, bottom=160),
      horizontal_align=types.HorizontalAlign.RIGHT,
      vertical_align=types.VerticalAlign.BOTTOM,
    )
    (text_left, text_top) = \
      text.get_text_position(self.image_draw, 'text', text_parameters, self.font)

    self.assertEqual(text_left, 90)
    self.assertEqual(text_top, 85)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])

class TestGetWatermarkPosition(unittest.TestCase):
  def setUp(self) -> None:
    self.image_draw = unittest.mock.create_autospec(ImageDraw.ImageDraw)
    self.font = ImageFont.load_default()

  def test_regular(self) -> None:
    self.image_draw.multiline_textbbox.side_effect = [(0, 0, 50, 10)]

    image_parameters = types.ImageParameters(width=640, height=480)
    (text_left, text_top) = \
      text.get_watermark_position(self.image_draw, 'text', image_parameters, self.font)

    self.assertEqual(text_left, 590)
    self.assertEqual(text_top, 470)
    self.image_draw.multiline_textbbox.assert_has_calls([
      unittest.mock.call((0, 0), 'text', self.font),
    ])
