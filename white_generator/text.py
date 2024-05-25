from . import types

def get_text_rectangle(image_parameters, text_parameters):
    rectangle = types.Rectangle(
        _crop(text_parameters.rectangle.left, 0, image_parameters.width),
        _crop(text_parameters.rectangle.top, 0, image_parameters.height),
        0,
        0,
    )
    if text_parameters.rectangle.right != -1:
        rectangle.right = _crop(
            text_parameters.rectangle.right,
            rectangle.left,
            image_parameters.width,
        )
    else:
        rectangle.right = image_parameters.width
    if text_parameters.rectangle.bottom != -1:
        rectangle.bottom = _crop(
            text_parameters.rectangle.bottom,
            rectangle.top,
            image_parameters.height,
        )
    else:
        rectangle.bottom = image_parameters.height

    return rectangle

def fit_text(draw, text, text_parameters, font):
    if text.strip() == '':
        return text

    lines = text.split('\n')
    if len(lines) > 1:
        return '\n'.join(
            fit_text(draw, line, text_parameters, font)
            for line in lines
        )

    words = [word.strip() for word in text.split(' ') if word.strip() != '']
    text = words[0]
    rectangle_width = \
        text_parameters.rectangle.right - text_parameters.rectangle.left
    for word in words[1:]:
        extended_text = text + ' ' + word
        (text_box_left, _, text_box_right, _) \
            = draw.multiline_textbbox((0, 0), extended_text, font=font)
        text_width = text_box_right - text_box_left
        if text_width <= rectangle_width:
            text = extended_text
        else:
            text = text + '\n' + word

    return text

def get_text_position(draw, text, text_parameters, font):
    (text_box_left, text_box_top, text_box_right, text_box_bottom) \
        = draw.multiline_textbbox((0, 0), text, font=font)
    text_width = text_box_right - text_box_left
    text_left = _get_text_position_on_axis(
        text_parameters.rectangle.left,
        text_parameters.rectangle.right,
        text_width,
        text_parameters.horizontal_align,
    )
    text_height = text_box_bottom - text_box_top
    text_top = _get_text_position_on_axis(
        text_parameters.rectangle.top,
        text_parameters.rectangle.bottom,
        text_height,
        text_parameters.vertical_align,
    )
    return (text_left, text_top)

def get_watermark_position(draw, text, image_parameters, font):
    (text_box_left, text_box_top, text_box_right, text_box_bottom) \
        = draw.multiline_textbbox((0, 0), text, font=font)
    text_width = text_box_right - text_box_left
    text_left = image_parameters.width - text_width
    text_height = text_box_bottom - text_box_top
    text_top = image_parameters.height - text_height
    return (text_left, text_top)

def _crop(value, minimum, maximum):
    return max(minimum, min(value, maximum))

def _get_text_position_on_axis(axis_start, axis_end, text_size, align):
    axis_size = axis_end - axis_start
    if align in [types.HorizontalAlign.LEFT, types.VerticalAlign.TOP]:
        position = 0
    elif align in [types.HorizontalAlign.CENTER, types.VerticalAlign.CENTER]:
        position = (axis_size - text_size) // 2
    elif align in [types.HorizontalAlign.RIGHT, types.VerticalAlign.BOTTOM]:
        position = axis_size - text_size
    else:
        raise Exception('the text alignment is incorrect')

    return position + axis_start
