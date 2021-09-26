from . import logger


class BaseSystemError(Exception):
    def __init__(self, message, status_code=500):
        self.message = message
        self.status_code = status_code
        logger.error(message)

    def __str__(self):
        return self.message


class RequestError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PydanticError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ImageProcessError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NoFaceDetectedError(Exception):
    def __init__(self, message):
        super().__init__(message)
