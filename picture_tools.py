import os
import exif
import shutil


def getPathsRecursively(folder_name):
    # TODO: Transform into non-recursive version?
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
                    split_path[-1] = generateNewFileName(image.datetime, split_path[-1],
                                                         keep_orig_name)
                else:
                    files_without_exif.append(path)
            except AssertionError:
                print('ERROR: File', path,
                      'does not seem to contain Exif',
                      'information. It will be copied')
                files_without_exif.append(path)

            new_paths.append('/'.join(split_path))

    return new_paths, files_without_exif


def renameFilesExif(source_folder, target_folder, keep_orig_name):
    assert(source_folder != target_folder)

    paths = getPathsRecursively(source_folder)

    new_paths, files_without_exif = generateNewPaths(paths, source_folder, target_folder,
                                                     keep_orig_name)

    if len(files_without_exif):
        print('The following files did not contain exif information and were just copied:')
        for name in files_without_exif:
            print(name)

    assert(len(paths) == len(new_paths))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for i in range(len(paths)):
        if not os.path.exists(os.path.dirname(new_paths[i])):
            os.makedirs(os.path.dirname(new_paths[i]), exist_ok=True)
        shutil.copy2(paths[i], new_paths[i])

    new_paths_check = getPathsRecursively(target_folder)

    assert(len(paths) == len(new_paths_check))
