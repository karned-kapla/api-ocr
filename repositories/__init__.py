from typing import Type

from common_api.services.v0 import Logger
from repositories.ocr_repository_mongo import OcrRepositoryMongo

logger = Logger()


class Repositories:
    def __init__(self, ocr_repo=None):
        self.ocr_repo = ocr_repo


class BucketRepositories:
    def __init__(self, ocr_bucket_repo=None):
        self.ocr_bucket_repo = ocr_bucket_repo


def get_repositories(uri: str) -> Repositories | Type[Repositories]:
    if uri.startswith("mongodb"):
        logger.info("Using MongoDB repositories")
        return Repositories(
            ocr_repo = OcrRepositoryMongo(uri)
        )

    return Repositories


def get_bucket_repositories(credentials) -> BucketRepositories | Type[BucketRepositories]:

    return BucketRepositories
