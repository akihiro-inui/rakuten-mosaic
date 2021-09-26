import os
from . import logger


def is_valid_file(uploaded_file_name: str):
    """
    Verify uploaded file format
    :param uploaded_file_name: Uploaded file name
    :return: True if the uploaded file is supported
    """
    is_valid_file = False
    try:
        if uploaded_file_name.endswith(tuple(os.environ.get("ALLOWED_UPLOAD_IMAGE_EXTENSION").split())):
            is_valid_file = True
    except Exception as err:
        logger.error(f"Unexpected error occurred while verifying the image file: {err}")
    finally:
        return is_valid_file
