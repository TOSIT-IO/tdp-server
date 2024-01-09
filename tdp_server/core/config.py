import os
from dotenv import load_dotenv
from pathlib import Path

from tdp.core.collection import Collection
from tdp.core.collections import Collections

load_dotenv("/home/sbaume-consultant01/Documents/tdp/tdp-getting-started/.env")


class Settings:
    TDP_DATABASE_DSN = os.getenv("TDP_DATABASE_DSN", None)
    TDP_COLLECTION_PATH = os.getenv("TDP_COLLECTION_PATH", None)
    TDP_RUN_DIRECTORY = Path(os.getenv("TDP_RUN_DIRECTORY", None))
    TDP_VARS = Path(os.getenv("TDP_VARS", None))


settings = Settings()

collections = Collections.from_collection_list(
    [
        Collection.from_path(col)
        for col in settings.TDP_COLLECTION_PATH.split(os.pathsep)
    ]
)
