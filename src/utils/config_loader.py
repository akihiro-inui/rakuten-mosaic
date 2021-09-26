import os
from dotenv import load_dotenv
from src.utils import logger


# Load .env file
# After this, you can access to environment like os.environ.get("VARIABLE")
def load_config(env_file_path: str) -> None:
    """
    Try to load environment variables from file path
    :param env_file_path: Path to the environment variable file
    """
    if os.path.isfile(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        logger.info(f".env file does not exist on {env_file_path}. Loading environment variable from the machine")

