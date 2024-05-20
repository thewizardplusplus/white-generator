import os
import sys

import termcolor

from . import logger
from . import cli
from . import io
from . import db
from . import types
from . import generation

def main():
    logger.init_logger()

    try:
        options = cli.parse_options()
        if not os.path.exists(options.output_path):
            os.makedirs(options.output_path)

        db_connection = db.connect_to_db(options.database_file)
        for note in io.read_notes(options.input_file):
            note_id = io.generate_note_id(note)
            logger.get_logger().info(
                'generate an image for the %s note',
                termcolor.colored(note_id, 'blue'),
            )

            if not db.exists_in_db(db_connection, note):
                db.insert_in_db(db_connection, note)
            else:
                logger.get_logger().warning(
                    'note %s is duplicated',
                    termcolor.colored(note_id, 'blue'),
                )
                continue

            image = generation.generate_image(
                note,
                types.ImageParameters(
                    width=options.image_width,
                    height=options.image_height,
                    background_color=options.image_background_color,
                    background_image=options.image_background_image,
                ),
                types.TextParameters(
                    font=types.FontParameters(
                        file=options.font_file,
                        size=options.font_size,
                        color=options.font_color,
                    ),
                    rectangle=types.Rectangle(
                        left=options.text_left,
                        top=options.text_top,
                        right=options.text_right,
                        bottom=options.text_bottom,
                    ),
                    horizontal_align=options.text_horizontal_align,
                    vertical_align=options.text_vertical_align,
                ),
                types.WatermarkParameters(
                    text=options.watermark_text,
                    size=options.watermark_size,
                    color=options.watermark_color,
                ),
            )
            image.save(
                os.path.join(options.output_path, note_id + '.png'),
                'PNG',
            )
    except Exception as exception:
        logger.get_logger().error(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
