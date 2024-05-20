import argparse
import pathlib

from . import __version__
from . import types

class HelpFormatter(
    argparse.RawTextHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter,
):
    pass

def parse_options():
    parser = argparse.ArgumentParser(
        prog=__package__.replace('_', '-'),
        formatter_class=HelpFormatter,
    )
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        help='show the version message and exit',
        version='White Generator, v{:s}\n'.format(__version__) \
            + 'Copyright (C) 2017 thewizardplusplus',
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
        default=types.DEFAULT_RECTANGLE_LEFT,
        help='the left text position',
    )
    parser.add_argument(
        '-t',
        '--text-top',
        type=int,
        default=types.DEFAULT_RECTANGLE_TOP,
        help='the top text position',
    )
    parser.add_argument(
        '-R',
        '--text-right',
        type=int,
        default=types.DEFAULT_RECTANGLE_RIGHT,
        help='the horizontal text limit (-1 for a background width use)',
    )
    parser.add_argument(
        '-B',
        '--text-bottom',
        type=int,
        default=types.DEFAULT_RECTANGLE_BOTTOM,
        help='the vertical text limit (-1 for a background height use)',
    )
    parser.add_argument(
        '-a',
        '--text-horizontal-align',
        choices=['left', 'center', 'right'],
        default='center',
        help='the text horizontal alignment',
    )
    parser.add_argument(
        '-A',
        '--text-vertical-align',
        choices=['top', 'center', 'bottom'],
        default='center',
        help='the text vertical alignment',
    )
    parser.add_argument(
        '-W',
        '--image-width',
        type=int,
        default=types.DEFAULT_IMAGE_WIDTH,
        help='the image width',
    )
    parser.add_argument(
        '-H',
        '--image-height',
        type=int,
        default=types.DEFAULT_IMAGE_HEIGHT,
        help='the image height',
    )
    parser.add_argument(
        '-b',
        '--image-background-color',
        default=types.DEFAULT_IMAGE_BACKGROUND_COLOR,
        help='the image background color',
    )
    parser.add_argument(
        '-I',
        '--image-background-image',
        type=pathlib.Path,
        help='the path to the background image',
    )
    parser.add_argument(
        '-f',
        '--font-file',
        type=pathlib.Path,
        required=True,
        help='the path to the font file',
    )
    parser.add_argument(
        '-s',
        '--font-size',
        type=int,
        default=types.DEFAULT_FONT_SIZE,
        help='the font size',
    )
    parser.add_argument(
        '-c',
        '--font-color',
        default=types.DEFAULT_FONT_COLOR,
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
