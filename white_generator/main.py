import logging
import os
import sys

from . import cli
from . import io
from . import db
from . import types
from . import generation

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

            image = generation.generate_image(
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
