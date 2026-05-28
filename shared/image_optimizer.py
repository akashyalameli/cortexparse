from PIL import Image


MAX_SIZE = 1600


def optimize_image(
    image_path: str
):

    image = Image.open(image_path)

    width, height = image.size

    scale = min(
        MAX_SIZE / width,
        MAX_SIZE / height,
        1
    )

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized = image.resize(
        (new_width, new_height)
    )

    resized.save(
        image_path,
        quality=85
    )

    return image_path
