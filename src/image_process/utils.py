import os
import cv2
import numpy as np
from src.utils import logger


def read_image(image_file):
    """
    Read image file as binary
    :param image_file: Image file
    :return: Binary image data
    """
    try:
        # Read image as binary
        file_bytes = np.asarray(bytearray(image_file._file.read()), dtype=np.uint8)
        image_data = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return image_data
    except Exception as err:
        logger.error(f"Failed to read the uploaded image file: {err}")


def resize_image(image_array: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Resize given binary image data
    :param image_array: Image data as numpy array
    :param width: Image width to resize
    :param height: Image height to resize
    :return: Resized image data array
    """
    try:
        return cv2.resize(image_array,
                          (width, height))
    except Exception as err:
        logger.error(f"Failed to read the uploaded image file: {err}")


def save_image(file_path: str, image_array: np.ndarray):
    """
    Save image data as file
    :param file_path: File path to write to
    :param image_array: Image data as numpy array
    """
    try:
        cv2.imwrite(file_path, image_array)
    except Exception as err:
        logger.error(f"Failed to save the image file: {err}")


def remove_image(file_path: str):
    """
    Delete image file
    :param file_path: File path to delete
    """
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)
        else:
            logger.error(f"Could not delete the file as it does not exist: {file_path}")
    except Exception as err:
        logger.error(f"Failed to delete the image file: {err}")
