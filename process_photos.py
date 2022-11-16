import os
from PIL import Image, ImageOps


def get_photo_names(photo_dir: str) -> list[str]:
    return [f for f in os.listdir(photo_dir) if os.path.isfile(os.path.join(photo_dir, f)) and not f.endswith(".json")]


def get_large_photo_names(photo_dir: str) -> list[str]:
    return sorted(f for f in get_photo_names(photo_dir) if "Small" not in f)


def process_photos(photo_dir: str, output_dir: str):

    photo_filenames = get_photo_names(photo_dir)

    for filename in photo_filenames:
        with open(os.path.join(photo_dir, filename), 'rb') as f:
            with Image.open(f) as img:
                img = ImageOps.exif_transpose(img)
                img.thumbnail((1024, 1024))
                img.save(os.path.join(output_dir, filename))

                name_without_ext, ext = os.path.splitext(filename)
                small_name = name_without_ext + "Small" + ext

                img.thumbnail((200, 200))
                img.save(os.path.join(output_dir, small_name))
