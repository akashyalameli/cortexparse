from minio import Minio

from shared.config.settings import settings


client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)


def ensure_bucket_exists():

    exists = client.bucket_exists(
        settings.MINIO_BUCKET
    )

    if not exists:

        client.make_bucket(
            settings.MINIO_BUCKET
        )
