import os
import uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def _blob_service_client() -> BlobServiceClient:
    conn_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if conn_string:
        return BlobServiceClient.from_connection_string(conn_string)

    account_url = os.environ["BLOB_ACCOUNT_URL"]
    return BlobServiceClient(account_url=account_url, credential=DefaultAzureCredential())


def upload_bytes(file_name: str, file_bytes: bytes) -> str:
    container_name = os.environ.get("BLOB_CONTAINER", "uploads")
    blob_name = f"uploads/{uuid.uuid4()}_{file_name}"

    blob_service = _blob_service_client()
    container_client = blob_service.get_container_client(container_name)
    if not container_client.exists():
        container_client.create_container()

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file_bytes, overwrite=True)

    return blob_client.url
