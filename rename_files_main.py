import argparse
from pathlib import Path

import picture_tools as pt

parser = argparse.ArgumentParser(
    description="Rename (and copy) images using exif information."
)
parser.add_argument("source_folder", help="Source folder", type=str)
parser.add_argument("target_folder", help="Target folder", type=str)

parser.add_argument(
    "--keep",
    dest="keep_orig_name",
    action="store_true",
    help="Flag whether original file name should be contained in new name.",
)
parser.set_defaults(keep_orig_name=False)
parser.add_argument(
    "--time_difference",
    dest="time_difference",
    help="Time difference to be added to exif timestamp in hours.",
    default=0,
    type=int,
)

args = parser.parse_args()

pt.rename_files_exif(
    Path(args.source_folder),
    Path(args.target_folder),
    args.keep_orig_name,
    args.time_difference,
)
