import os
import exif  # type: ignore
import shutil
import logging
from typing import Optional
from pathlib import Path
from PIL import Image, ExifTags  # type: ignore


def generateNewFileName(exif_datetime: str, file_name: str, keep_orig_name: bool) -> str:
    """Generate new file name using exif date-time information.

    Args:
        exif_datetime: Date-time string
        file_name: Input file name
        keep_orig_name: Flag whether the original file name should be part of the new file name

    Returns:
        New file name
    """
    img_datetime = exif_datetime.replace(':', '-').replace(' ', '_')

    if keep_orig_name:
        file_name = img_datetime + '_' + file_name
    else:
        file_ending = file_name.split('.')[-1]
        file_name = img_datetime + '.' + file_ending

    return file_name


def get_exif_creation_date(img_path: Path) -> Optional[str]:
    """Get exif creation date from file.

    Args:
        img_path: Path to file

    Returns:
        Exif creation date-time as string, None if no exif information is available
    """
    with open(img_path, 'rb') as file:
        try:
            image = exif.Image(file)

            if image.has_exif:
                return image.datetime_original

            else:
                print(f"INFO: File {img_path} does not seem to contain Exif information. It will be copied.")
                return None

        except AssertionError:
            print(f"INFO: File {img_path} does not seem to contain Exif information. It will be copied.")
            return None


def rename_files_exif(source_folder: Path, target_folder: Path, keep_orig_name: bool) -> None:
    """Rename files using exif date-time information.

    Args:
        source_folder: Folder to read files from
        target_folder: Folder for renamed files
        keep_orig_name: Flag whether original file name should be part of the new file name
    """
    assert source_folder != target_folder, "Program needs to be run with different source and target folders"

    for root, _, files in os.walk(source_folder):
        for file in files:
            path: Path = Path(root) / file

            exif_creation_date: Optional[str] = get_exif_creation_date(path)

            if exif_creation_date is not None:
                new_file_name = generateNewFileName(exif_creation_date, path.name, keep_orig_name)
            else:
                new_file_name = path.name

            new_path: Path = Path(str(path).replace(str(source_folder), str(target_folder)))
            new_path = new_path.parent / new_file_name

            if not new_path.parent.exists():
                new_path.parent.mkdir(exist_ok=True)

            if new_path.exists():
                print(f"File with path {new_path} already exists. Appending '.1' to avoid overwriting.")
                new_path = Path(str(new_path) + '.1')

            shutil.copy2(path, new_path)
