#!/usr/bin/env python3

import argparse
import sqlite3

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class ImageParameters:
    def __init__(self, width, height, background_color):
        self.width = width
        self.height = height
        self.background_color = background_color

class FontParameters:
    def __init__(self, file_, size, color):
        self.file = file_
        self.size = size
        self.color = color

class WatermarkParameters:
    def __init__(self, text, size, color):
        self.text = text
        self.size = size
        self.color = color

def parse_options():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='White Generator, v1.0 (Copyright (C) 2017 thewizardplusplus)',
    )
    parser.add_argument(
        '-W',
        '--image-width',
        type=int,
        default=640,
        help='the image width',
    )
    parser.add_argument(
        '-H',
        '--image-height',
        type=int,
        default=480,
        help='the image height',
    )
    parser.add_argument(
        '-b',
        '--image-background-color',
        default='#ffffff',
        help='the image background color',
    )
    parser.add_argument(
        '-f',
        '--font-file',
        required=True,
        help='the path to the font file',
    )
    parser.add_argument(
        '-s',
        '--font-size',
        type=int,
        default=25,
        help='the font size',
    )
    parser.add_argument(
        '-c',
        '--font-color',
        default='#000000',
        help='the font color',
    )
    parser.add_argument(
        '-w',
        '--watermark-text',
        default='',
        help='the watermark text (empty for disable)',
    )
    parser.add_argument(
        '-S',
        '--watermark-size',
        type=int,
        default=12,
        help='the watermark font size',
    )
    parser.add_argument(
        '-C',
        '--watermark-color',
        default='#808080',
        help='the watermark font color',
    )
    parser.add_argument(
        '-d',
        '--database-file',
        default='notes.db',
        help='the path to the database file',
    )

    return parser.parse_args()

def connect_to_db(db_file):
    db_connection = sqlite3.connect(db_file)
    db_connection \
        .cursor() \
        .execute(
            '''
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    text TEXT NOT NULL UNIQUE
                )
            '''
        )
    db_connection.commit()

    return db_connection

def insert_in_db(db_connection, text):
    db_connection.cursor().execute('INSERT INTO notes(text) VALUES(?)', (text,))
    db_connection.commit()

def exists_in_db(db_connection, text):
    (counter,) = db_connection \
        .cursor() \
        .execute('SELECT count(*) FROM notes WHERE text = ?', (text,)) \
        .fetchone()
    return bool(counter)

def get_text_position(draw, text, image_parameters, font):
    (text_width, text_height) = draw.multiline_textsize(text, font=font)
    text_left = (image_parameters.width - text_width) / 2
    text_top = (image_parameters.height - text_height) / 2
    return (text_left, text_top)

def get_watermark_position(draw, text, image_parameters, font):
    (text_width, text_height) = draw.textsize(text, font=font)
    text_left = image_parameters.width - text_width
    text_top = image_parameters.height - text_height
    return (text_left, text_top)

def generate_image(
    text,
    image_parameters,
    font_parameters,
    watermark_parameters,
):
    image = Image.new(
        'RGB',
        (image_parameters.width, image_parameters.height),
        image_parameters.background_color,
    )
    draw = ImageDraw.Draw(image)
    text_font = ImageFont.truetype(font_parameters.file, font_parameters.size)
    draw.multiline_text(
        get_text_position(draw, text, image_parameters, text_font),
        text,
        align='center',
        font=text_font,
        fill=font_parameters.color,
    )

    if len(watermark_parameters.text) != 0:
        watermark_font = ImageFont.truetype(
            font_parameters.file,
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

options = parse_options()
db_connection = connect_to_db(options.database_file)
if not exists_in_db(db_connection, 'test'):
    insert_in_db(db_connection, 'test')
    print('inserts the "test" text')
else:
    print('the "test" text already exists')
if not exists_in_db(db_connection, 'ololo'):
    insert_in_db(db_connection, 'ololo')
    print('inserts the "ololo" text')
else:
    print('the "ololo" text already exists')
db_connection.close()
