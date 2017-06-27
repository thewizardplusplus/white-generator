import logging
import os
import sys

from . import cli
from . import io
from . import db
from . import types
from . import generation

def main():
    try:
        logging.basicConfig(
            format='%(asctime)s\t[%(levelname)s]\t%(message)s',
            level=logging.INFO,
        )

        options = cli.parse_options()
        if not os.path.exists(options.output_path):
            os.makedirs(options.output_path)

        db_connection = None
        try:
            db_connection = db.connect_to_db(options.database_file)
            for note in io.read_notes(options.input_file):
                note_id = io.generate_note_id(note)
                logging.info(
                    "it's generating an image for the note %s",
                    note_id,
                )

                if not db.exists_in_db(db_connection, note):
                    db.insert_in_db(db_connection, note)
                else:
                    logging.warning("the note %s is duplicated", note_id)
                    continue

                image = generation.generate_image(
                    note,
                    types.ImageParameters(options),
                    types.TextParameters(options),
                    types.WatermarkParameters(options),
                )
                image.save(
                    os.path.join(options.output_path, note_id + '.png'),
                    'PNG',
                )
        finally:
            db.close_connection_to_db(db_connection)
    except Exception as exception:
        logging.critical(exception)
        sys.exit(1)
    except KeyboardInterrupt:
        # output a line break after the ^C symbol in a terminal
        print('')

        sys.exit(1)
