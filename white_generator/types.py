class ImageParameters:
    def __init__(self, width, height, background_color, background_image):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.background_image = background_image

class FontParameters:
    def __init__(self, file_, size, color):
        self.file = file_
        self.size = size
        self.color = color

class Rectangle:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

class TextParameters:
    def __init__(self, font, rectangle, horizontal_align, vertical_align):
        self.font = font
        self.rectangle = rectangle
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align

class WatermarkParameters:
    def __init__(self, text, size, color):
        self.text = text
        self.size = size
        self.color = color
