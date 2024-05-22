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
