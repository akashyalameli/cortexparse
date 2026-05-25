from pathlib import Path

from minio.error import S3Error

from shared.config.settings import settings
from shared.minio_client import client


def upload_document(
    object_name: str,
    file_path: str
):

    client.fput_object(
        settings.MINIO_BUCKET,
        object_name,
        file_path
    )

    return object_name


def delete_document(
    object_name: str
):

    try:

        client.remove_object(
            settings.MINIO_BUCKET,
            object_name
        )

    except S3Error:

        pass
