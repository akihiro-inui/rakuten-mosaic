import os
import cv2
import hashlib
import numpy as np
import face_recognition
from src.utils import logger
from src.utils.custom_error_handlers import NoFaceDetectedError
from src.image_process.utils import read_image, resize_image, save_image, remove_image


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
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_image = image_array[:, :, ::-1]

        # Find all the faces from the given image file
        face_locations = face_recognition.face_locations(rgb_image)

        # If no face is detected, raise error
        if len(face_locations) == 0:
            raise NoFaceDetectedError("No face was detected")

        # Apply mosaic effect to all detected faces
        for top, right, bottom, left in face_locations:
            # Resize to small size (mosaic)
            small = cv2.resize(image_array[top:bottom, left:right],
                               None,
                               fx=0.05,
                               fy=0.05,
                               interpolation=cv2.INTER_NEAREST)

            # Resize back to original size (face area)
            image_array[top:bottom, left:right] = cv2.resize(small,
                                                             image_array[top:bottom, left:right].shape[:2][::-1],
                                                             interpolation=cv2.INTER_NEAREST)
        return image_array

    except NoFaceDetectedError:
        logger.info("No face was detected")
        raise NoFaceDetectedError("No face was detected")

