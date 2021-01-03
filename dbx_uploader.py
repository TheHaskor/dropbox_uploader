import dropbox
from pathlib import Path
import sys
import os
import re

auth_token = 'enter your auth token here'
dbx = dropbox.Dropbox(auth_token)
dropbox_root_dir = 'root_dir - make sure it exists'

class UploadFile:
    def __init__(self, file_name, locate_relative_path, destination_relative_path):
        self.file_name = file_name
        self.locate_relative_path = locate_relative_path
        self.destination_relative_path = destination_relative_path


##############################
# files to upload to dropbox #
##############################


files_to_upload = [
    UploadFile("^name1.*tar.gz", r'rel1', r'dest1'),  # Starts with 'name1' and ends with 'tar.gz'
    UploadFile("^name2.*exe$", r'', r''),
    UploadFile("^name3.*dll", r'', r''),
    ]

def get_full_destination(find_file, name):
    dest = Path(os.path.join(os.path.join(dropbox_root_dir, find_file.destination_relative_path), name))
    dest_string = f'/{dest}'.replace('\\', '/')
    return dest_string


def upload_file(file_from, file_to):
    with open(file_from, "rb") as f:
        dbx.files_upload(f.read(), file_to)


if __name__ == '__main__':
    base_dir = Path(sys.argv[1])
    for find_file in files_to_upload:
        find_path = os.path.join(base_dir, find_file.locate_relative_path)
        file_found = False
        for file in os.listdir(find_path):
            if re.search(find_file.file_name, file):
                print(f'uploading {file} matching {find_file.file_name} regex to {find_file.destination_relative_path}')
                full_location = os.path.join(find_path, file)
                full_destination = get_full_destination(find_file, file)
                upload_file(full_location, full_destination)
                print('file uploaded')
                file_found = True
        if not file_found:
            raise Exception(f'did not find file {find_file.file_name} in {find_file.locate_relative_path}')
