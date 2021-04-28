import pathlib
import re
import os
from urllib import request, parse
from sys import stdout

# regex_for_normalize_filename = re.compile('[/*?:"<>|]')
regex_for_normalize_filename = re.compile('[^A-Za-z0-9]+')


def _normalize(file_name: str):
    return re.sub(regex_for_normalize_filename, "_", file_name)


def download_file(folder_name: str, file_link: str, output_file_name: str):
    folder_name = os.path.join('downloaded', _normalize(folder_name))
    output_file_name = _normalize(output_file_name)
    if not pathlib.Path(folder_name).is_dir():
        os.makedirs(folder_name)
        print(f'folder "{folder_name}" created')
    _, file_extension = os.path.splitext(parse.urlparse(file_link).path)
    song_file_path_no_ext = os.path.join(folder_name, output_file_name)
    song_file_path_with_ext = os.path.join(folder_name, output_file_name + file_extension)
    if pathlib.Path(song_file_path_no_ext).is_file():  # file download was incomplete before
        os.remove(song_file_path_no_ext)
        os.remove(song_file_path_with_ext)

    if pathlib.Path(song_file_path_with_ext).is_file():
        print(f'file "{output_file_name}" ignored because downloaded before')
    else:
        open(song_file_path_no_ext, 'a').close()  # create temp file
        stdout.write(f'file "{output_file_name}" is downloading...')
        stdout.flush()
        request.urlretrieve(file_link, song_file_path_with_ext)
        stdout.write(f'\x1b[2K\rfile "{output_file_name}" downloaded\n')
        stdout.flush()
        os.remove(song_file_path_no_ext)
