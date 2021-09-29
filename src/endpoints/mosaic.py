from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from src.utils import logger
from src.utils.custom_error_handlers import RequestError
from src.utils.verify_file_type import is_valid_file
from src.image_process.utils import remove_image
from src.image_process.apply_mosaic import process
from starlette.responses import FileResponse
from starlette.background import BackgroundTasks

router = APIRouter()


@router.post("/mosaic")
async def mosaic(background_tasks: BackgroundTasks, image_file: UploadFile = File(...), ) -> JSONResponse:
    """
    Process uploaded image file.
    1. Verify request type is correct
    2. Verify file extension is supported
    3. Resize ans save the converted image file
    :return: StreamingResponse(200) or JSONResponse(500)
    """
    try:
        # Verify file extension is supported
        valid = is_valid_file(image_file.filename)
        if not valid:
            raise RequestError(f"This file format is not supported: {image_file.file}")

        # Apply mosaic effect to the uploaded image file
        processed_image_file_path = process(image_file.file)
        background_tasks.add_task(remove_image, processed_image_file_path)
        return FileResponse(processed_image_file_path, status_code=200)

    except Exception as err:
        logger.error(f"Process image failed: {err}")
        return JSONResponse(status_code=500,
                            content={"data": {},
                                     "message": f"Could not process the image: {err}"})