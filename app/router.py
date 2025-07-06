import os
import uuid

from app.schema import IncludeSpanishRequest, IncludeSpanishResponse
from app.service import generate_with_spanish_translations, create_import_file_string, process_files, create_import_file

from fastapi import APIRouter, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse

from app.settings import settings

router = APIRouter()
@router.get("/")
async def root():
    return {"message": "My API"}


@router.post('/propresenter/include_spanish')
async def include_spanish(request: IncludeSpanishRequest) -> IncludeSpanishResponse:
    structured_response = await generate_with_spanish_translations(texts=[request.text])
    importable_file = create_import_file_string(structured_raw_file=structured_response)
    print(importable_file)
    return IncludeSpanishResponse(text_data=importable_file, json_data=structured_response)


@router.post('/propresenter/upload_exported_files')
async def create_upload_files(files: list[UploadFile], background_tasks: BackgroundTasks):
    folder_name = str(uuid.uuid4())
    processed_folder_path = f"{settings.project_dir}/data/processed/{folder_name}"
    if not os.path.exists(processed_folder_path):
        os.makedirs(processed_folder_path)
    processed_files = process_files(raw_files=[file.file.read() for file in files], processed_folder_path=processed_folder_path)
    import_file_path = f"{processed_folder_path}/importable_file.txt"
    background_tasks.add_task(create_import_file, structured_raw_file=processed_files, importable_file_path=import_file_path)
    return {"file_id": folder_name}


@router.get('/propresenter/download_importable_file/{file_id}')
async def download_importable_file(file_id: str):
    folder_path = f"{settings.project_dir}/data/processed/{file_id}"
    file_path = f"{folder_path}/importable_file.txt"
    if not os.path.exists(file_path):
        return {"message": "File not found"}
    return FileResponse(file_path)