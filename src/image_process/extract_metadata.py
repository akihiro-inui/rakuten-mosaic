import os
import hashlib
from deepface import DeepFace
from src.image_process.utils import read_image, save_image


def process(original_image) -> dict:
    """
    Read image file, resize and apply mosaic effect
    :param original_image: Original image as SpooledTemporaryFile
    :return metadata: dictionary {"age": int,
                                  "race": str,
                                  "emotion": str,
                                  "image_file_path": str}
    """
    # Placeholder
    metadata = {"age": None, "race": None, "emotion": None, "image_file_path": None}

    # Read image file
    image_binary = read_image(original_image)

    # Hash original image
    sha256 = hashlib.sha256(image_binary).hexdigest()

    # Save mosaic image
    original_image_file_path = os.path.join(os.environ.get("UPLOAD_FOLDER"), f"{sha256}.png")
    save_image(original_image_file_path, image_binary)

    # Use Deep face analyzer to extract age, gender, race and emotion
    extracted_metadata = DeepFace.analyze(img_path=original_image_file_path,
                                          actions=['age', 'gender', 'race', 'emotion'])

    metadata["age"] = extracted_metadata["age"]
    metadata["race"] = extracted_metadata["dominant_race"]
    metadata["emotion"] = extracted_metadata["dominant_emotion"]
    metadata["image_file_path"] = original_image_file_path

    return metadata
