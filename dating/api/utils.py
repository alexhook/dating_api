from PIL import Image
from io import BytesIO
from typing import Union
from pathlib import Path
from django.core.files import File
from math import radians, sin, cos, acos


def validate_img_size(image: File, min_size: tuple):
    """"
    Returns True if image size greater than
    min_size values.

    :param image: File object of image.
    :param min_size: Minimum width and height values.
    """
    with Image.open(image) as im:
        w, h = im.size
        try:
            w_min, h_min = min_size
            w_min = int(w_min)
            h_min = int(h_min)
        except (TypeError, ValueError):
            raise AssertionError('The "min_size" must be a tuple instance.')

        return w >= w_min and h >= h_min


def add_watermark(image: File, wm_path: Union[str, Path], wm_dividor: Union[int, float], indent: tuple, file_format: str):
    """"
    Adds a watermark to the original image.

    :param image: File object of main image.
    :param wm_path: Path of watermark image.
    :param wm_dividor: How many times is it 
    necessary to reduce watermark size relative to 
    the smallest side of the main image.
    :param indent: Watermark indent from right-botom 
    corner of main image.
    :param file_format: File format for result image.
    """
    with Image.open(image) as im, Image.open(wm_path) as wm:
        wm_size = min(im.size) // wm_dividor
        wm.thumbnail((wm_size, wm_size))

        x = im.size[0] - wm.size[0] - indent[0]
        y = im.size[1] - wm.size[1] - indent[1]

        im.paste(wm, (x, y), mask=wm)

        image_io = BytesIO()
        if not file_format == 'PNG':
            im = im.convert('RGB')
        im.save(image_io, file_format)

        img_name, img_ext = image.name.split('.')
        result = File(
            image_io,
            name='.'.join((img_name, file_format.lower())))

        return result


def great_circle(lat1, lon1, lat2, lon2):
    """"
    Returns geo distance between two Earth points.
    """
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    return 6371 * acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon1 - lon2))