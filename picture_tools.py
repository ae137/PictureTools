import os
import exif
import shutil
import logging
from typing import Optional
from pathlib import Path
from PIL import Image, ExifTags


def getPathsRecursively(folder_name):
    # TODO: Use glob.rglob or os.path.walk!
    files = []
    folder_content = os.listdir(folder_name)
    for entry in folder_content:
        path = os.path.join(folder_name, entry)
        if os.path.isfile(path):
            files.append(path)
        else:
            files.extend(getPathsRecursively(os.path.join(folder_name, entry)))
    return files


def generateNewFileName(exif_datetime, file_name, keep_orig_name):
    img_datetime = exif_datetime.replace(':', '-').replace(' ', '_')

    if keep_orig_name:
        file_name = img_datetime + '_' + file_name
    else:
        file_ending = file_name.split('.')[-1]
        file_name = img_datetime + '.' + file_ending

    return file_name


def generateNewPaths(paths, source_folder, target_folder, keep_orig_name):
    new_paths = []
    files_without_exif = []

    for path in paths:
        new_path = path.replace(source_folder, target_folder)

        split_path = new_path.split('/')

        with open(path, 'rb') as file:
            print(path)

            try:
                image = exif.Image(file)

                if image.has_exif:
                    split_path[-1] = generateNewFileName(image.datetime_original, split_path[-1],
                                                         keep_orig_name)
                else:
                    files_without_exif.append(path)
            except (AttributeError, AssertionError):
                print('ERROR: File', path,
                      'does not seem to contain Exif',
                      'information. It will be copied')
                files_without_exif.append(path)

            new_paths.append('/'.join(split_path))

    return new_paths, files_without_exif


def get_exif_creation_date(img_path: Path) -> Optional[Path]:
    with open(img_path, 'rb') as file:
        image = exif.Image(file)

        if image.has_exif:
            return image.datetime_original

        else:
            print(f"INFO: File {img_path} does not seem to contain Exif information. It will be copied.")
            return None


def renameFilesExif(source_folder, target_folder, keep_orig_name):
    assert source_folder != target_folder, "Program needs to be run with different source and target folders"

    for root, _, files in os.walk(source_folder):
        for file in files:
            path = Path(root) / file

            exif_creation_date = get_exif_creation_date(path)

            new_path = Path(str(path).replace(source_folder, target_folder))

            if exif_creation_date is not None:
                new_file_name = generateNewFileName(exif_creation_date, new_path.name, keep_orig_name)
            else:
                new_file_name = new_path.name

            new_path = new_path.parent / new_file_name

            if not new_path.parent.exists():
                new_path.parent.mkdir(exist_ok=True)
            shutil.copy2(path, new_path)
