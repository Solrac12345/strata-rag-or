"""
EN: S3 helper for uploading / downloading knowledge-base files.
FR: Utilitaire S3 pour charger / télécharger les fichiers de la base de connaissances.
"""
from __future__ import annotations

import os

try:
    import boto3  # type: ignore
except Exception:  # pragma: no cover
    boto3 = None


class S3Storage:
    """
    EN: Thin wrapper around boto3 S3 client.
        Falls back to no-op stubs when boto3 is unavailable.
    FR: Couche mince autour du client S3 boto3.
        Retourne des stubs no-op quand boto3 n'est pas disponible.
    """

    def __init__(self, bucket: str | None = None, region: str | None = None) -> None:
        self.bucket = bucket or os.getenv("S3_BUCKET", "strata-rag-kb")
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self._client = None
        if boto3 is not None:
            self._client = boto3.client("s3", region_name=self.region)

    def upload(self, key: str, data: bytes) -> bool:
        if self._client is None:
            return False
        self._client.put_object(Bucket=self.bucket, Key=key, Body=data)
        return True

    def download(self, key: str) -> bytes | None:
        if self._client is None:
            return None
        resp = self._client.get_object(Bucket=self.bucket, Key=key)
        return resp["Body"].read()

    def list_keys(self, prefix: str = "") -> list[str]:
        if self._client is None:
            return []
        resp = self._client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        return [obj["Key"] for obj in resp.get("Contents", [])]