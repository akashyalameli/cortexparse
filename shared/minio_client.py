import json
from io import BytesIO

from minio import Minio
from minio.error import S3Error

from shared.config.settings import settings
from shared.default_templates import templates


client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)


def ensure_bucket(bucket_name: str):

    exists = client.bucket_exists(
        bucket_name
    )

    if not exists:

        client.make_bucket(
            bucket_name
        )


def ensure_templates_exist():

    try:

        client.stat_object(
            settings.MINIO_TEMPLATE_BUCKET,
            "logo.json"
        )

        return

    except S3Error as ex:

        if ex.code not in {
            "NoSuchKey",
            "NoSuchBucket",
        }:
            raise

    ensure_bucket(
        settings.MINIO_TEMPLATE_BUCKET
    )

    for object_name, template in templates.items():

        template_bytes = json.dumps(
            template,
            indent=2
        ).encode("utf-8")

        client.put_object(
            settings.MINIO_TEMPLATE_BUCKET,
            object_name,
            BytesIO(template_bytes),
            len(template_bytes),
            content_type="application/json"
        )
