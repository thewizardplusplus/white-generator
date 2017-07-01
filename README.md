# White Generator

Utility for a generation of memes.

## Features

* a generation of memes (in PNG format);
* a support of plain and graphic backgrounds;
* a specification of a text rectangle;
* a support of horizontal and vertical text alignments;
* a read of memes texts from a file (each text is separated from another by a double newline);
* a support single-line and multiline memes texts;
* a protection against duplicate memes texts;
* a support of a watermark (it's optional);
* meme settings:
    * background:
        * color;
        * width;
        * height;
        * image (it supports same formats as [Pillow](http://python-pillow.org/) library);
    * text:
        * font (it supports only TrueType fonts);
        * size;
        * color;
        * left;
        * rigth;
        * top;
        * bottom;
        * horizontal alignment;
        * vertical alignment;
    * watermark:
        * font (it always uses the text font);
        * text;
        * size;
        * color.

## Installation

```
$ pip install white-generator
```

## Usage

```
$ white-generator -v | --version
$ white-generator -h | --help
$ white-generator [options] (-f FONT_FILE | --font-file FONT_FILE) (-i INPUT_FILE | --input-file INPUT_FILE) (-o OUTPUT_PATH | --output-path OUTPUT_PATH)
```

Options:

* `-v`, `--version` &mdash; show the version message and exit;
* `-h`, `--help` &mdash; show this help message and exit;
* `-i INPUT_FILE`, ` --input-file INPUT_FILE` &mdash; the path to the file with notes;
* `-o OUTPUT_PATH`, ` --output-path OUTPUT_PATH` &mdash; the path for generated images;
* `-l TEXT_LEFT`, ` --text-left TEXT_LEFT` &mdash; the left text position (default: 0);
* `-t TEXT_TOP`, ` --text-top TEXT_TOP` &mdash; the top text position (default: 0);
* `-R TEXT_RIGHT`, ` --text-right TEXT_RIGHT` &mdash; the horizontal text limit (-1 for a background width use; default: -1);
* `-B TEXT_BOTTOM`, ` --text-bottom TEXT_BOTTOM` &mdash; the vertical text limit (-1 for a background height use; default: -1);
* `-a {left,center,right}`, ` --text-horizontal-align {left,center,right}` &mdash; the text horizontal alignment (default: `center`);
* `-A {top,center,bottom}`, ` --text-vertical-align {top,center,bottom}` &mdash; the text vertical alignment (default: `center`);
* `-W IMAGE_WIDTH`, ` --image-width IMAGE_WIDTH` &mdash; the image width (default: 640);
* `-H IMAGE_HEIGHT`, ` --image-height IMAGE_HEIGHT` &mdash; the image height (default: 480);
* `-b IMAGE_BACKGROUND_COLOR`, ` --image-background-color IMAGE_BACKGROUND_COLOR` &mdash; the image background color (default: `#ffffff`);
* `-I IMAGE_BACKGROUND_IMAGE`, ` --image-background-image IMAGE_BACKGROUND_IMAGE` &mdash; the path to the background image (default: none);
* `-f FONT_FILE`, ` --font-file FONT_FILE` &mdash; the path to the font file;
* `-s FONT_SIZE`, ` --font-size FONT_SIZE` &mdash; the font size (default: 25);
* `-c FONT_COLOR`, ` --font-color FONT_COLOR` &mdash; the font color (default: `#000000`);
* `-w WATERMARK_TEXT`, ` --watermark-text WATERMARK_TEXT` &mdash; the watermark text (empty for disable; default: empty);
* `-S WATERMARK_SIZE`, ` --watermark-size WATERMARK_SIZE` &mdash; the watermark font size (default: 12);
* `-C WATERMARK_COLOR`, ` --watermark-color WATERMARK_COLOR` &mdash; the watermark font color (default: `#808080`);
* `-d DATABASE_FILE`, ` --database-file DATABASE_FILE` &mdash; the path to the database file (default: `notes.db`).

## Screenshots

![Help message, part 1](screenshots/screenshot_01.png)

Help message, part 1

![Help message, part 2](screenshots/screenshot_02.png)

Help message, part 2

![Generation of images](screenshots/screenshot_03.png)

Generation of images

![Generated image](screenshots/screenshot_04.png)

Generated image

## License

The MIT License (MIT)

Copyright &copy; 2017 thewizardplusplus
