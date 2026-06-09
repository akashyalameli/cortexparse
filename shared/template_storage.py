import json

from minio.error import S3Error

from shared.config.settings import settings
from shared.minio_client import client
from shared.minio_client import ensure_bucket


SUPPORTED_TEMPLATE_NAMES = {
    "logo",
    "pan",
    "aadhaar",
    "form",
    "prescription",
    "receipt",
    "invoice",
}


class TemplateNotFoundError(Exception):
    pass


def ensure_template_bucket_exists():

    ensure_bucket(
        settings.MINIO_TEMPLATE_BUCKET
    )


def load_template_schema(
    template_name: str
):

    object_name = f"{template_name}.json"
    response = None

    try:

        response = client.get_object(
            settings.MINIO_TEMPLATE_BUCKET,
            object_name
        )

        template_bytes = response.read()

    except S3Error as ex:

        if ex.code in {
            "NoSuchBucket",
            "NoSuchKey",
        }:
            raise TemplateNotFoundError(
                f"Template '{template_name}' was not found in MinIO bucket '{settings.MINIO_TEMPLATE_BUCKET}'"
            ) from ex

        raise

    finally:

        if response is not None:
            response.close()
            response.release_conn()

    return json.loads(
        template_bytes.decode("utf-8")
    )
