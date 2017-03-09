import logging
import os
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from . import cli
from . import io
from . import db

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

def crop(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def get_text_rectangle(image_parameters, text_parameters):
    rectangle = Rectangle(
        crop(text_parameters.rectangle.left, 0, image_parameters.width),
        crop(text_parameters.rectangle.top, 0, image_parameters.height),
        0,
        0,
    )
    if text_parameters.rectangle.right != -1:
        rectangle.right = crop(
            text_parameters.rectangle.right,
            rectangle.left,
            image_parameters.width,
        )
    else:
        rectangle.right = image_parameters.width
    if text_parameters.rectangle.bottom != -1:
        rectangle.bottom = crop(
            text_parameters.rectangle.bottom,
            rectangle.top,
            image_parameters.height,
        )
    else:
        rectangle.bottom = image_parameters.height

    return rectangle

def fit_text(draw, text, text_parameters, font):
    if len(text.strip()) == 0:
        return text

    lines = text.split('\n')
    if len(lines) > 1:
        return '\n'.join(
            fit_text(draw, line, text_parameters, font)
            for line in lines,
        )

    words = [word.strip() for word in text.split(' ') if len(word.strip()) != 0]
    text = words[0]
    rectangle_width = text_parameters.rectangle.right \
        - text_parameters.rectangle.left
    for word in words[1:]:
        extended_text = text + ' ' + word
        (text_width, _) = draw.multiline_textsize(extended_text, font=font)
        if text_width <= rectangle_width:
            text = extended_text
        else:
            text = text + '\n' + word

    return text

def get_text_position_on_axis(axis_start, axis_end, text_size, align):
    axis_size = axis_end - axis_start
    if align in ['left', 'top']:
        position = 0
    elif align == 'center':
        position = (axis_size - text_size) // 2
    elif align in ['right', 'bottom']:
        position = axis_size - text_size
    else:
        raise Exception('the text align is incorrect')

    return position + axis_start

def get_text_position(draw, text, text_parameters, font):
    (text_width, text_height) = draw.multiline_textsize(text, font=font)
    text_left = get_text_position_on_axis(
        text_parameters.rectangle.left,
        text_parameters.rectangle.right,
        text_width,
        text_parameters.horizontal_align,
    )
    text_top = get_text_position_on_axis(
        text_parameters.rectangle.top,
        text_parameters.rectangle.bottom,
        text_height,
        text_parameters.vertical_align,
    )
    return (text_left, text_top)

def get_watermark_position(draw, text, image_parameters, font):
    (text_width, text_height) = draw.textsize(text, font=font)
    text_left = image_parameters.width - text_width
    text_top = image_parameters.height - text_height
    return (text_left, text_top)

def generate_image(
    text,
    image_parameters,
    text_parameters,
    watermark_parameters,
):
    if len(image_parameters.background_image) == 0:
        image = Image.new(
            'RGB',
            (image_parameters.width, image_parameters.height),
            image_parameters.background_color,
        )
    else:
        image = Image.open(image_parameters.background_image)
        (image_parameters.width, image_parameters.height) = image.size
    text_parameters.rectangle = get_text_rectangle(
        image_parameters,
        text_parameters,
    )

    draw = ImageDraw.Draw(image)
    text_font = ImageFont.truetype(
        text_parameters.font.file,
        text_parameters.font.size,
    )
    text = fit_text(draw, text, text_parameters, text_font)
    draw.multiline_text(
        get_text_position(draw, text, text_parameters, text_font),
        text,
        align=text_parameters.horizontal_align,
        font=text_font,
        fill=text_parameters.font.color,
    )

    if len(watermark_parameters.text) != 0:
        watermark_font = ImageFont.truetype(
            text_parameters.font.file,
            watermark_parameters.size,
        )
        draw.text(
            get_watermark_position(
                draw,
                watermark_parameters.text,
                image_parameters,
                watermark_font,
            ),
            watermark_parameters.text,
            font=watermark_font,
            fill=watermark_parameters.color,
        )

    return image

def main():
    logging.basicConfig(
        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
        level=logging.INFO
    )

    try:
        options = cli.parse_options()
        if not os.path.exists(options.output_path):
            os.makedirs(options.output_path)

        db_connection = db.connect_to_db(options.database_file)
        for note in io.read_notes(options.input_file):
            note_id = io.generate_note_id(note)
            logging.info("it's generating an image for the note %s", note_id)

            if not db.exists_in_db(db_connection, note):
                db.insert_in_db(db_connection, note)
            else:
                logging.warning("the note %s is duplicated", note_id)
                continue

            image = generate_image(
                note,
                ImageParameters(
                    options.image_width,
                    options.image_height,
                    options.image_background_color,
                    options.image_background_image,
                ),
                TextParameters(
                    FontParameters(
                        options.font_file,
                        options.font_size,
                        options.font_color,
                    ),
                    Rectangle(
                        options.text_left,
                        options.text_top,
                        options.text_right,
                        options.text_bottom,
                    ),
                    options.text_horizontal_align,
                    options.text_vertical_align,
                ),
                WatermarkParameters(
                    options.watermark_text,
                    options.watermark_size,
                    options.watermark_color,
                )
            )
            image.save(
                os.path.join(options.output_path, note_id + '.png'),
                'PNG'
            )
    except Exception as exception:
        logging.critical(exception)
        sys.exit(1)
