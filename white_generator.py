#!/usr/bin/env python3

import uuid
import argparse
import sqlite3
import logging
import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

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

class TextParameters:
    def __init__(
        self,
        font,
        left,
        top,
        right,
        bottom,
        horizontal_align,
        vertical_align,
    ):
        self.font = font
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.horizontal_align = horizontal_align
        self.vertical_align = vertical_align

class WatermarkParameters:
    def __init__(self, text, size, color):
        self.text = text
        self.size = size
        self.color = color

_UUID_NAMESPACE = uuid.uuid1()

def parse_options():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='White Generator, v1.1 (Copyright (C) 2017 thewizardplusplus)',
    )
    parser.add_argument(
        '-i',
        '--input-file',
        required=True,
        help='the path to the file with notes',
    )
    parser.add_argument(
        '-o',
        '--output-path',
        required=True,
        help='the path for generated images',
    )
    parser.add_argument(
        '-l',
        '--text-left',
        type=int,
        default=0,
        help='the left text position',
    )
    parser.add_argument(
        '-t',
        '--text-top',
        type=int,
        default=0,
        help='the top text position',
    )
    parser.add_argument(
        '-R',
        '--text-right',
        type=int,
        default=-1,
        help='the horizontal text limit (-1 for a background width use)',
    )
    parser.add_argument(
        '-B',
        '--text-bottom',
        type=int,
        default=-1,
        help='the vertical text limit (-1 for a background height use)',
    )
    parser.add_argument(
        '-a',
        '--text-horizontal-align',
        choices=['left', 'center', 'right'],
        default='center',
        help='the text horizontal align',
    )
    parser.add_argument(
        '-A',
        '--text-vertical-align',
        choices=['top', 'center', 'bottom'],
        default='center',
        help='the text vertical align',
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
        '-I',
        '--image-background-image',
        default='',
        help='the path to the background image',
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

def read_notes(notes_filename):
    with open(notes_filename, 'r') as notes_file:
        note = ''
        for line in notes_file:
            if len(line.rstrip()) != 0:
                note += line.rstrip() + '\n'
            elif len(note.rstrip()) != 0:
                yield note.rstrip()
                note = ''

        if len(note.rstrip()) != 0:
            yield note.rstrip()

def generate_note_id(note):
    return str(uuid.uuid5(_UUID_NAMESPACE, note))

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

    draw = ImageDraw.Draw(image)
    text_font = ImageFont.truetype(
        text_parameters.font.file,
        text_parameters.font.size,
    )
    draw.multiline_text(
        (text_parameters.left, text_parameters.top),
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

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s\t[%(levelname)s]\t%(message)s',
        level=logging.INFO
    )

    try:
        options = parse_options()
        if not os.path.exists(options.output_path):
            os.makedirs(options.output_path)

        db_connection = connect_to_db(options.database_file)
        for note in read_notes(options.input_file):
            note_id = generate_note_id(note)
            logging.info("it's generating an image for the note %s", note_id)

            if not exists_in_db(db_connection, note):
                insert_in_db(db_connection, note)
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
                    options.text_left,
                    options.text_top,
                    options.text_right,
                    options.text_bottom,
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
