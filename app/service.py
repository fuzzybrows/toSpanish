import json
import os
import logging

from google.genai import Client as GenAIClient
from google.genai.errors import ServerError

from app.settings import settings
from app.schema import Song, SongsParentModel, VerseType

logger = logging.getLogger(__name__)

BATCH_SIZE = 15

LYRICS_PROMPT = ("Convert each line of this json list of raw song files excluding the title line(denoted by 'Title:') and any empty lines into spanish. "
              "Verses are denoted by 'Verse' and chorus is denoted by 'Chorus' if no verses are explicitly labelled, group verses based by multiple consecutive line breaks. Ensure the title line is not converted to spanish. If no title is explicitly defined, try to identify and use the title of the song found online. if unsuccessful, copy the first line as the title. Verse labels could be just a name like 'Verse' or a numbered name like 'Verse 1' same for all the other verse labels. Use these labels to build the output but remove them from the text")

GENAI_CLIENT =  GenAIClient(api_key=settings.genai_client_api_key)


def retrieve_unprocessed_files():
    folder_path = f"{settings.project_dir}/data/unprocessed"
    file_names = [f for f in os.listdir(folder_path) if not os.path.isdir(os.path.join(folder_path, f))]
    files = []
    for file_name in file_names:
        with open(f"{folder_path}/{file_name}", 'r') as file:
            lines = file.readlines()
            files.append(lines)
    return files


def process_files(start_index: int = 0,
                  batch_size: int = BATCH_SIZE,
                  raw_files=None,
                  processed_folder_path: str = f"{settings.project_dir}/data/processed/general",
                  write_to_file: bool = False):
    raw_files = raw_files or retrieve_unprocessed_files()
    processed_files = SongsParentModel(songs=[])

    files_length = len(raw_files)
    end_index = start_index + batch_size
    should_loop = True
    while should_loop:
        if end_index >= files_length:
            end_index = files_length
            should_loop = False
        logger.info(
            f"Processing... start_index={start_index}, end_index={end_index}, total_length_of_files={files_length}")
        response = get_gemini_reponse(prompt=LYRICS_PROMPT, values=raw_files[start_index:end_index])

        if not response.parsed:
            logger.info(f"Failed to obtain parsed data for batch. start_index={start_index}, end_index={end_index}, batch_size={batch_size}")
            processed_files2 = process_files(batch_size=batch_size // 2, raw_files=raw_files[start_index:end_index], processed_folder_path=processed_folder_path)
            processed_files.songs.extend(processed_files2.songs)
        else:
            processed_files.songs.extend(response.parsed)

        start_index = end_index - 1
        end_index += batch_size

    if write_to_file:
        with open(f"{processed_folder_path}/all_processed_files.json", "w") as all_processed_files:
            all_processed_files.write(SongsParentModel.model_dump_json(processed_files))
    return processed_files


def get_gemini_reponse(prompt: str, values: list[str], retry_count: int = 0):
    try:
        return GENAI_CLIENT.models.generate_content(
            model="gemini-2.0-flash", contents=f"{prompt}. VALUES={values}",
            config={
                "response_mime_type": "application/json",
                "response_schema": list[Song],
            }
        )
    except ServerError as e:
        if "The model is overloaded. Please try again later." in e:
            if retry_count > 5:
                raise e
            retry_attempt = retry_count + 1
            logger.info("Retrying... Attempt No: " + str(retry_attempt))
            return get_gemini_reponse(prompt, values, retry_attempt)
        raise e



def generate_with_spanish_translations(texts: list[str]) -> SongsParentModel:
    response = get_gemini_reponse(prompt=LYRICS_PROMPT, values=texts)
    return SongsParentModel.model_validate({"songs": response.parsed})

def create_import_file(structured_raw_file: SongsParentModel, importable_file_path: str):
    with open(f"{importable_file_path}", "w") as import_file:
        import_file.write(create_import_file_string(structured_raw_file))


def create_import_file_string(structured_raw_file: SongsParentModel):
    import_ready_file = ""
    for song in structured_raw_file.songs:
        import_ready_file += f"Title: {song.title}-(WITH-SPANISH)\n\n"
        verse_number = 0
        for verse in song.verses:
            if verse.type is VerseType.VERSE:
                verse_number += 1
                import_ready_file += f"{verse.type.name.title()} {verse_number}\n"
            else:
                import_ready_file += f"{verse.type.name.title()}\n"
            for line in verse.lines:
                import_ready_file += f"{line.english}\n"
                if line.spanish is not None:
                    import_ready_file += f"({line.spanish})\n"
                else:
                    import_ready_file += "\n"
            import_ready_file += "\n"
        import_ready_file += "\n"
    return import_ready_file





