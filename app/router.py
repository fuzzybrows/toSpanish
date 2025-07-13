import logging
import os
import uuid

from pydantic_core._pydantic_core import ValidationError

from app.schema import IncludeSpanishRequest, IncludeSpanishResponse, SongsParentModel
from app.service import generate_with_spanish_translations, create_import_file_string, process_files, create_import_file

from fastapi import APIRouter, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse

from app.settings import settings


logger = logging.getLogger(__name__)
router = APIRouter()
@router.get("/")
async def root():
    return {"message": "My API"}


@router.post('/propresenter/include_spanish')
def include_spanish(request: IncludeSpanishRequest) -> IncludeSpanishResponse:
    structured_response = generate_with_spanish_translations(texts=[request.text])
    importable_file = create_import_file_string(structured_raw_file=structured_response)
    print(importable_file)
    return IncludeSpanishResponse(text_data=importable_file, json_data=structured_response)


@router.post('/propresenter/upload_exported_files')
def create_upload_files(files: list[UploadFile], background_tasks: BackgroundTasks):
    folder_name = str(uuid.uuid4())
    processed_folder_path = f"{settings.project_dir}/data/processed/{folder_name}"
    if not os.path.exists(processed_folder_path):
        os.makedirs(processed_folder_path)
    background_tasks.add_task(process_files_background,
                              raw_files={file.filename: file.file.read() for file in files},
                              processed_folder_path=processed_folder_path)
    return {"file_id": folder_name}

def process_files_background(raw_files: dict[str, bytes | str], processed_folder_path: str):
    with open(f"{settings.project_dir}/data/songs_database.json", "r") as songs_database:
        try:
            db = SongsParentModel.model_validate_json(songs_database.read())
        except (ValidationError, Exception) as e:
            logger.exception(f"Validation error: {e}")
            db = SongsParentModel(songs=[])
    try:
        processed_files = process_files(raw_files=raw_files,
                                        processed_folder_path=processed_folder_path,
                                        write_to_file=True,
                                        songs_db=db)
    except Exception as e:
        logger.exception(f"Error processing files: {e}")
        with open(f"{settings.project_dir}/data/songs_database.json", "w") as songs_database:
            songs_database.write(db.model_dump_json(exclude={"songs_by_title": True}))
        raise
    else:
        with open(f"{settings.project_dir}/data/songs_database.json", "w") as songs_database:
            songs_database.write(db.model_dump_json(exclude={"songs_by_title": True}))
        import_file_path = f"{processed_folder_path}/importable_file.txt"
        create_import_file(structured_raw_file=processed_files, importable_file_path=import_file_path)






@router.get('/propresenter/download_importable_file/{file_id}')
def download_importable_file(file_id: str):
    folder_path = f"{settings.project_dir}/data/processed/{file_id}"
    file_path = f"{folder_path}/importable_file.txt"
    if not os.path.exists(file_path):
        return {"message": "File not found"}
    return FileResponse(file_path)