import unittest

from . import types

class TestColor(unittest.TestCase):
  def test_parse_rgb(self) -> None:
    color = types.Color.parse('rgb(12, 23, 42)')
    self.assertEqual(color, types.Color(red=12, green=23, blue=42))

  def test_parse_rgb_hex(self) -> None:
    color = types.Color.parse('#0c172a')
    self.assertEqual(color, types.Color(red=12, green=23, blue=42))

  def test_parse_rgb_hex_short(self) -> None:
    color = types.Color.parse('#abc')
    self.assertEqual(color, types.Color(red=170, green=187, blue=204))

  def test_parse_rgba(self) -> None:
    color = types.Color.parse('rgba(5, 12, 23, 42)')
    self.assertEqual(color, types.Color(red=5, green=12, blue=23, alpha=42))

  def test_parse_rgba_hex(self) -> None:
    color = types.Color.parse('#050c172a')
    self.assertEqual(color, types.Color(red=5, green=12, blue=23, alpha=42))

  def test_parse_rgba_hex_short(self) -> None:
    color = types.Color.parse('#abcd')
    self.assertEqual(color, types.Color(red=170, green=187, blue=204, alpha=221))

  def test_parse_error(self) -> None:
    with self.assertRaises(ValueError):
      types.Color.parse('invalid-color')
