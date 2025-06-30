from app.schema import IncludeSpanishRequest, IncludeSpanishResponse
from app.service import generate_with_spanish_translations, create_import_file, process_files

from fastapi import APIRouter

router = APIRouter()
@router.get("/")
async def root():
    return {"message": "Include Spanish API"}

@router.post('/propresenter/include_spanish')
async def include_spanish(request: IncludeSpanishRequest) -> IncludeSpanishResponse:
    structured_response = generate_with_spanish_translations(texts=[request.text])
    importable_file = create_import_file(structured_raw_file=structured_response)
    return IncludeSpanishResponse(text_data=importable_file, json_data=structured_response)


@router.get('/process')
async def process_files_request():
    return process_files()
