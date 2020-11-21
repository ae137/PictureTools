import pytest  # type: ignore
import os
from pathlib import Path
from typing import Optional, Tuple

import picture_tools as pt


@pytest.fixture
def test_filename_generation_inputs() -> Tuple[str, str]:
    datetime_example = '2019:12:29 21:44:22'
    file_name = 'IMG_4600.JPG'

    return datetime_example, file_name


def test_generate_file_name_keep(test_filename_generation_inputs: Tuple[str, str]):
    """Check returned filename in case the old one should be kept."""

    datetime_example, filename_input = test_filename_generation_inputs
    new_file_name_keep = '2019-12-29_21-44-22_IMG_4600.JPG'

    assert new_file_name_keep == pt.generateNewFileName(datetime_example, filename_input, True, 0)


def test_generate_file_name_keep_not_correct_time(test_filename_generation_inputs: Tuple[str, str]):
    """Check returned filename in case the old one should be kept."""

    datetime_example, filename_input = test_filename_generation_inputs
    new_file_name_keep_not = '2019-12-29_22-44-22.JPG'

    assert new_file_name_keep_not == pt.generateNewFileName(datetime_example, filename_input, False, 1)


def test_generate_file_name_keep_not(test_filename_generation_inputs: Tuple[str, str]):
    """Check returned filename in case the old one should be kept."""

    datetime_example, filename_input = test_filename_generation_inputs
    new_file_name_keep_not = '2019-12-29_21-44-22.JPG'

    assert new_file_name_keep_not == pt.generateNewFileName(datetime_example, filename_input, False, 0)


def test_get_exif_creation_date_success_simple() -> None:
    """Check that exif creation date is correct for file with exif information."""

    path: Path = Path('test/subdir/IMG_4600.JPG')
    expected_exif_date: str = "2019:06:21 15:42:21"

    result: Optional[str] = pt.get_exif_creation_date(path)
    assert result is not None, "Got None as result when Optional should have a value"

    assert result == expected_exif_date, f"Obtained wrong result {result}. Should be {expected_exif_date}"


def test_get_exif_creation_date_fail_simple() -> None:
    """Check that exif creation date is None for file without exif information."""

    path: Path = Path('test/fileWithoutExif.txt')
    result: Optional[str] = pt.get_exif_creation_date(path)

    assert result is None, "Got string when Optional should be None"


def test_rename_files_exif_keep_not(tmp_path: Path) -> None:
    """Check that correct folder structure is produced when original file names should not be kept."""
    source_folder: Path = Path("test")
    target_folder: Path = tmp_path

    pt.rename_files_exif(source_folder, target_folder, False)

    assert (target_folder / "fileWithoutExif.txt").exists()
    assert (target_folder / "subdir" / "2019-06-21_15-42-21.JPG").exists()


def test_rename_files_exif_keep(tmp_path: Path) -> None:
    """Check that correct folder structure is produced when original file names should be kept."""
    source_folder: Path = Path("test")
    target_folder: Path = tmp_path

    pt.rename_files_exif(source_folder, target_folder, True)

    assert (target_folder / "fileWithoutExif.txt").exists()
    assert (target_folder / "subdir" / "2019-06-21_15-42-21_IMG_4600.JPG").exists()
