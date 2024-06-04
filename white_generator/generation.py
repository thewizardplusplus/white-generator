import pathlib

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from . import text
from . import types

def generate_image(
    note: str,
    image_parameters: types.ImageParameters,
    text_parameters: types.TextParameters,
    watermark_parameters: types.WatermarkParameters,
) -> Image.Image:
    if image_parameters.background_image is None:
        image = Image.new(
            'RGB',
            (image_parameters.width, image_parameters.height),
            tuple(image_parameters.background_color),
        )
    else:
        image = Image.open(image_parameters.background_image)
        (image_parameters.width, image_parameters.height) = image.size

    text_parameters.rectangle = text.fit_text_rectangle(
        image_parameters,
        text_parameters,
    )

    draw = ImageDraw.Draw(image)
    text_font = load_font(text_parameters.font.file, text_parameters.font.size)
    fitted_note = text.fit_text(draw, note, text_parameters, text_font)
    draw.multiline_text(
        text.get_text_position(draw, fitted_note, text_parameters, text_font),
        fitted_note,
        align=text_parameters.horizontal_align,
        font=text_font,
        fill=tuple(text_parameters.font.color),
    )

    if watermark_parameters.text is not None:
        watermark_font = load_font(
            text_parameters.font.file,
            watermark_parameters.size,
        )
        draw.multiline_text(
            text.get_watermark_position(
                draw,
                watermark_parameters.text,
                image_parameters,
                watermark_font,
            ),
            watermark_parameters.text,
            font=watermark_font,
            fill=tuple(watermark_parameters.color),
        )

    return image

def load_font(
    font_file: pathlib.Path | None,
    font_size: int,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if font_file is None:
        return ImageFont.load_default(font_size)

    return ImageFont.truetype(font_file, font_size)
