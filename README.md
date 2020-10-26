# PictureTools

## Renaming of image files using exif information
### Renaming of images files according to date and time information from exif
Rename an image file, for example `IMG_4600.JPG` into `2019-06-21_15-42-21.JPG` using the time stamp in the exif 
information.

### Examples
* `python3 rename_files_main.py test test_renamed`

    yields new file names based on the time stamp in the exif information, for example `2019-06-21_15-42-21.JPG`

* `python3 rename_files_main.py test test_renamed --keep`

    yields new file names that combine the time stamp in the exif information with the old file name, for 
    example `2019-06-21_15-42-21_IMG_4600.JPG`
