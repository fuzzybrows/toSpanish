import json
import os
import logging

from google import genai

from app.settings import settings
from app.schema import Song, SongsParentModel, VerseType

logger = logging.getLogger(__name__)

BATCH_SIZE = 15

LYRICS_PROMPT = ("Convert each line of this json list of raw song files excluding the title line(denoted by 'Title:') and any empty lines into spanish. "
              "Verses are denoted by 'Verse' and chorus is denoted by 'Chorus' if no verses are explicitly labelled, group verses based by multiple consecutive line breaks. Ensure the title line is not converted to spanish. If no title is explicitly defined, try to identify and use the title of the song found online. if unsuccessful, copy the first line as the title. Verse labels could be just a name like 'Verse' or a numbered name like 'Verse 1' same for all the other verse labels. Use these labels to build the output but remove them from the text")

GENAI_CLIENT =  genai.Client(api_key=settings.genai_client_api_key)


def retrieve_unprocessed_files():
    folder_path = f"{settings.project_dir}/data/unprocessed"
    file_names = [f for f in os.listdir(folder_path) if not os.path.isdir(os.path.join(folder_path, f))]
    files = []
    for file_name in file_names:
        with open(f"{folder_path}/{file_name}", 'r') as file:
            lines = file.readlines()
            files.append(lines)
    return files

# def retrieve_missed2_files():
#     folder_path = f"{settings.project_dir}/data/unprocessed"
#     file_names = [f for f in os.listdir(folder_path) if not os.path.isdir(os.path.join(folder_path, f))]
#     missed2_files = [
#         "There is none like You"
#     ]
#     files = []
#     for file_name in file_names:
#         if file_name.split('.')[0] in missed2_files:
#             with open(f"{folder_path}/{file_name}", 'r') as file:
#                 lines = file.readlines()
#                 files.append(lines)
#     return files


# def retrieve_missed_files():
#     unprocessed_folder_path = f"{settings.project_dir}/data/unprocessed"
#     processed_folder_path = f"{settings.project_dir}/data/processed"
#     file_names = [f for f in os.listdir(unprocessed_folder_path) if not os.path.isdir(os.path.join(unprocessed_folder_path, f))]
#     files = []
#     for f in os.listdir(processed_folder_path):
#         if not os.path.isdir(os.path.join(processed_folder_path, f)) and not os.path.getsize(f"{processed_folder_path}/{f}"):
#             print("}}}}", f)
#             mat = re.search(r"(\d*)-(\d+)", f)
#             print("]]]]]", mat)
#             start_index = int(mat.group(1))
#             end_index = int(mat.group(2))
#
#             for file_name in file_names[start_index:end_index]:
#                 with open(f"{unprocessed_folder_path}/{file_name}", 'r') as file:
#                     lines = file.readlines()
#                     files.append(lines)
#     return files


def process_files(start_index: int = 0,
                  batch_size: int = BATCH_SIZE,
                  raw_files=None,
                  processed_folder_path: str = f"{settings.project_dir}/data/processed/general",
                  write_to_file: bool = False):
    raw_files = raw_files or retrieve_unprocessed_files()
    processed_files = SongsParentModel(songs=[])

    files_length = len(raw_files)
    end_index = start_index + batch_size
    if end_index > files_length:
        end_index = files_length
    should_loop = True
    while should_loop:
        logger.info(
            f"Processing... start_index={start_index}, end_index={end_index}, total_length_of_files={files_length}")
        if end_index >= files_length:
            end_index = files_length
            should_loop = False
        response = get_gemini_reponse(prompt=LYRICS_PROMPT, values=raw_files[start_index:end_index])

        if not response.parsed:
            logger.info(f"Failed to obtain parsed data for batch. start_index={start_index}, end_index={end_index}, batch_size={batch_size}")
            processed_files2 = process_files(batch_size=batch_size // 2, raw_files=raw_files[start_index:end_index], processed_folder_path=processed_folder_path)
            processed_files.songs.extend(processed_files2.songs)
            # processed_files.songs.extend(response.parsed) if response.parsed else []
            # skipped_files.extend(raw_files[start_index:end_index])
        else:
            processed_files.songs.extend(response.parsed)

        start_index = end_index - 1
        end_index += batch_size

    if write_to_file:
        with open(f"{processed_folder_path}/all_processed_files.json", "w") as all_processed_files:
            all_processed_files.write(SongsParentModel.model_dump_json(processed_files))
    return processed_files


# def rename_processed_files():
#     def update_numbering(match: re.Match):
#         return f"_{int(match.group(1))-10}-{int(match.group(2))-10}"
#
#     folder_path = f"{settings.project_dir}/data/processed"
#     for f in sorted(os.listdir(folder_path)):
#         if not os.path.isdir(os.path.join(folder_path, f)):
#             new = re.sub(r"(\d*)-(\d+)", update_numbering, f)
#             print(f"old: {f}, new: {new}")
#             os.rename(f"{folder_path}/{f}", f"{folder_path}/{new}")


# def process_missed_files(start_index: int = 0):
#     files = retrieve_missed2_files()
#     processed_files = Response(songs=[])
#     print("+++++", len(files))
#
#     files_length = len(files)
#     end_index = start_index + BATCH_SIZE
#     if end_index > files_length:
#         end_index = files_length
#     should_loop = True
#     while should_loop:
#         print("+++++++", f"start={start_index}, end={end_index}, total_length={files_length}")
#         if end_index >= files_length:
#             end_index = files_length
#             should_loop = False
#         response = get_gemini_reponse(prompt=LYRICS_PROMPT, values=files[start_index:end_index])
#
#         processed_files.songs.extend(response.parsed) if response.parsed else []
#         print("======", response.parsed)
#         with (
#             open(f"processed-missed10-parsed_batch{start_index}-{end_index}.json", "w") as parsed_file,
#             open(f"processed-missed10-text_batch{start_index}-{end_index}.json", "w") as text_file,
#         ):
#             text_file.write(response.text)
#             if response.parsed:
#                 parsed_file.write(Response.model_validate({"songs": response.parsed}).model_dump_json())
#
#         start_index = end_index
#         end_index += BATCH_SIZE
#
#     with open("data/sunday_all_processed_missed10_files.json", "w") as all_processed_files:
#         all_processed_files.write(Response.model_dump_json(processed_files))
#     return processed_files




def combine_files():
    with(
        open("data/all_processed_files.json", "r") as file1,
        open("data/all_processed_missed_files.json", "r") as file2,
        open("data/all_processed_missed_missed2_files.json", "r") as file3,
        open("data/all_processed_combined_files.json", "w") as combined_file
    ):
        a = file1.read()
        b = file2.read()
        c = file3.read()
        combined1 = SongsParentModel.model_validate_json(a)
        combined2 = SongsParentModel.model_validate_json(b)
        combined3 = SongsParentModel.model_validate_json(c)

        print("+++", len(combined1.songs), len(combined2.songs), len(combined3.songs))

        combined1.songs.extend(combined2.songs)
        combined1.songs.extend(combined3.songs)
        print("===", len(combined1.songs))

        combined_file.write(combined1.model_dump_json())


def find_unprocessed_songs():
    with open("data/all_processed_combined_files.json", "r") as combined_files:
        combined_object = SongsParentModel.model_validate_json(combined_files.read())

        titles = [song.title for song in combined_object.songs]
        print("+=+=", len(titles), len(set(titles)))
        sorted_list = sorted(list(set(titles)))

    folder_path = f"{settings.project_dir}/data/unprocessed"
    file_names = [f for f in os.listdir(folder_path) if not os.path.isdir(os.path.join(folder_path, f))]
    files = []
    missing = []
    for file_name in file_names:
        if file_name.split('.')[0] not in titles:
            missing.append(file_name)
            with open(f"{folder_path}/{file_name}", 'r') as file:
                lines = file.readlines()
                files.append(lines)
    with (
        open("data/total_list.json", 'w') as total_list,
        open("data/missing.json", 'w') as missing_list
    ):
        sorted_missing = sorted(list(set(missing)))
        print("JJJJ", sorted_missing)
        total_list.write(json.dumps(sorted_list))
        missing_list.write(json.dumps(sorted_missing))
    return files


def get_gemini_reponse(prompt: str, values: list[str]):
    return GENAI_CLIENT.models.generate_content(
        model="gemini-2.0-flash", contents=f"{prompt}. VALUES={values}",
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Song],
        }
    )


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





