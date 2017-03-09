import logging
import os
import sys

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from . import cli
from . import io
from . import db
from . import types
from . import text

def generate_image(
    note,
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
    text_parameters.rectangle = text.get_text_rectangle(
        image_parameters,
        text_parameters,
    )

    draw = ImageDraw.Draw(image)
    text_font = ImageFont.truetype(
        text_parameters.font.file,
        text_parameters.font.size,
    )
    fitted_note = text.fit_text(draw, note, text_parameters, text_font)
    draw.multiline_text(
        text.get_text_position(draw, fitted_note, text_parameters, text_font),
        fitted_note,
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
            text.get_watermark_position(
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
                types.ImageParameters(
                    options.image_width,
                    options.image_height,
                    options.image_background_color,
                    options.image_background_image,
                ),
                types.TextParameters(
                    types.FontParameters(
                        options.font_file,
                        options.font_size,
                        options.font_color,
                    ),
                    types.Rectangle(
                        options.text_left,
                        options.text_top,
                        options.text_right,
                        options.text_bottom,
                    ),
                    options.text_horizontal_align,
                    options.text_vertical_align,
                ),
                types.WatermarkParameters(
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
