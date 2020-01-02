
import picture_tools as pt
import argparse


parser = argparse.ArgumentParser(description='Rename (and copy) images using exif information.')
parser.add_argument('source_folder', help='Source folder')
parser.add_argument('target_folder', help='Target folder')

parser.add_argument('--keep', dest='keep_orig_name', action='store_true',
                    help='Flag whether original file name should be contained in new name.')
parser.set_defaults(keep_orig_name=False)

args = parser.parse_args()

pt.renameFilesExif(args.source_folder, args.target_folder, args.keep_orig_name)
