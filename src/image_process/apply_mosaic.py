import os
import hashlib
import numpy as np
from src.utils import logger
from src.image_process.utils import read_image, resize_image, save_image, detect_multiple_face_location
from src.image_process.blur import blur_image_locally


def process(original_image_file: str) -> str:
    """
    Read image file, resize and apply mosaic effect
    :param original_image_file: Original image file name
    """
    # Read image file
    image_binary = read_image(original_image_file)

    # Resize image
    image_size = int(os.environ.get("IMAGE_SIZE"))
    resized_image = resize_image(image_binary, width=image_size, height=image_size)

    # Hash original image
    sha256 = hashlib.sha256(image_binary).hexdigest()

    # Apply mosaic effect
    mosaic_image = apply_mosaic(resized_image)
    mosaic_image = resize_image(mosaic_image, width=image_binary.shape[1], height=image_binary.shape[0])

    # Save mosaic image
    processed_image_file_path = os.path.join(os.environ.get("UPLOAD_FOLDER"), f"{sha256}.png")
    save_image(processed_image_file_path, mosaic_image)

    return processed_image_file_path


def apply_mosaic(image_array: np.ndarray) -> np.ndarray:
    """
    Apply mosaic effect to the faces
    :param image_array: Image data as numpy array
    :return: Image data with mosaic effect applied to all faces
    """
    try:
        width = image_array.shape[1]
        height = image_array.shape[0]

        # # Find all the faces from the given image file
        face_locations = detect_multiple_face_location(image_array)

        # Create mask where 0 is blur 1 is non-blur part
        sharp_mask = np.full((width, height, 3), fill_value=1)

        # Apply mosaic effect to all detected faces
        for top, right, bottom, left in face_locations:
            # Set blur part to 0
            sharp_mask[top:bottom, left:right, :] = 0

            # Apply blur effect to detected face location
            image_array = blur_image_locally(
                image_array,
                sharp_mask,
                use_gaussian_blur=True,
                gaussian_sigma=13,
                uniform_filter_size=150)

        return image_array
    except Exception as err:
        logger.error(f"Something unexpected happened: {err}")