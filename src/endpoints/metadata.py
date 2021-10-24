from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from src.utils import logger
from src.utils.custom_error_handlers import RequestError
from src.utils.verify_file_type import is_valid_file
from src.image_process.utils import remove_image
from src.image_process.extract_metadata import process
from starlette.background import BackgroundTasks

router = APIRouter()


@router.post("/metadata")
async def metadata(background_tasks: BackgroundTasks, image_file: UploadFile = File(...), ) -> JSONResponse:
    """
    Process uploaded image file.
    1. Verify request type is correct
    2. Verify file extension is supported
    3. Detect emotion, age, race and emotion from image and return as json response
    :return: StreamingResponse(200) or JSONResponse(500)
    """
    try:
        # Verify file extension is supported
        valid = is_valid_file(image_file.filename)
        if not valid:
            raise RequestError(f"This file format is not supported: {image_file.file}")

        # Extract metadata from image file
        metadata = process(image_file.file)

        # Delete tmp file
        background_tasks.add_task(remove_image, metadata["image_file_path"])

        del metadata["image_file_path"]
        return JSONResponse(status_code=200,
                            content={"data": metadata,
                                     "message": f"Successfully analyzed image"})

    except Exception as err:
        logger.error(f"Process image failed: {err}")
        return JSONResponse(status_code=500,
                            content={"data": {},
                                     "message": f"Could not process the image: {err}"})