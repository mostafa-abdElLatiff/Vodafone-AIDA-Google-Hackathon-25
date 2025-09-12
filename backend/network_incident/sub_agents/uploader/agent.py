# app.py
import io
import mimetypes
from pathlib import Path
from typing import Optional
 
from google.adk.agents import Agent
from google.adk.tools import FunctionTool, ToolContext
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types  # Part/Blob used by ADK Artifacts
 
# -------------------------------
# Fixed GCS targets (as requested)
# -------------------------------
BUCKET_NAME = "aida-hackathon-team-5"
PREFIX = "uploaded_files"  # change to 'uploaded_filesand' if that was not a typo
 
# Robust MIME mapping for spreadsheets & CSV
EXT_MIME = {
    ".csv":  "text/csv",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls":  "application/vnd.ms-excel",
    ".xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    ".ods":  "application/vnd.oasis.opendocument.spreadsheet",
}
 
def resolve_mime(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    mime = EXT_MIME.get(ext)
    if not mime:
        guessed, _ = mimetypes.guess_type(filename)
        mime = guessed or "application/octet-stream"
    return mime
 
def _gcs_object_name(prefix: str, filename: str) -> str:
    """Build 'prefix/filename' robustly (no double slashes, no leading slash)."""
    prefix = (prefix or "").lstrip("/").rstrip("/")
    return f"{prefix}/{filename}" if prefix else filename
 
def process_and_upload_raw(
    filename: str,
    file_bytes: bytes,
    tool_context: ToolContext,
) -> dict:
    """
    Save the file as an ADK Artifact (GCS-backed) and upload the exact same bytes to:
      gs://aida-hackathon-team-5/uploaded_files/
 
    - Preserves original format (Excel/CSV/etc).
    - No re-encoding or transformation.
 
    Returns: JSON with status, artifact version, mime_type, size, and the GCS URI.
    """
    # 1) Save AS-IS as an Artifact (versioned)
    mime = resolve_mime(filename)
    part = types.Part.from_bytes(data=file_bytes, mime_type=mime)
    version = tool_context.save_artifact(filename=filename, artifact=part)
 
    # 2) Upload the SAME BYTES to the fixed bucket/prefix
    from google.cloud import storage
    size_bytes = len(file_bytes)
 
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    object_name = _gcs_object_name(PREFIX, filename)  # e.g., uploaded_files/
 
    blob = bucket.blob(object_name)
    # No transformation: upload raw bytes with correct content type
    blob.upload_from_file(io.BytesIO(file_bytes), size=size_bytes, content_type=mime)
 
    uploaded_to = f"gs://{BUCKET_NAME}/{object_name}"
 
    return {
        "status": "success",
        "filename": filename,
        "artifact_version": int(version),
        "mime_type": mime,
        "size_bytes": size_bytes,
        "uploaded_to": uploaded_to,
    }
 
process_and_upload_raw_tool = FunctionTool(func=process_and_upload_raw)
 
# -------------------------------
# Agent that will call the tool
# -------------------------------
uploader_agent = Agent(
    model="gemini-2.0-flash",
    name="file_uploader_agent",
    instruction=(
        "When the user attaches a file, call `process_and_upload_raw` with:\n"
        "- filename: the file's original name\n"
        "- file_bytes: the raw file bytes\n"
        "After uploading, reply with 'uploaded_to' and basic metadata."
    ),
    tools=[process_and_upload_raw_tool],
)
 
# -------------------------------
# Runner wiring: GCS-backed Artifacts
# -------------------------------
# Uses GCS so Artifact versions persist across sessions.
try:
    from google.adk.artifacts import GcsArtifactService
except ImportError:
    # Some ADK versions locate it under gcs_artifact_service
    from google.adk.artifacts.gcs_artifact_service import GcsArtifactService  # type: ignore
 
gcs_artifact_service = GcsArtifactService(bucket_name=BUCKET_NAME)
 
session_service = InMemorySessionService()
runner = Runner(
    agent=uploader_agent,
    app_name="uploader_app",
    session_service=session_service,
    artifact_service=gcs_artifact_service,  # <-- artifacts saved to your GCS bucket
)