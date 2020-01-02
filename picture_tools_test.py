import unittest
import os
import picture_tools as pt


class TestGetPathList(unittest.TestCase):
    def test_simple(self):
        correct = ['test/IMG_4600.JPG', 'test/fileWithoutExif.txt']
        actual = pt.getPathsRecursively('test')

        self.assertEqual(len(actual), len(correct))
        self.assertEqual(actual.sort(), correct.sort())


class TestGenerateNewFileName(unittest.TestCase):
    def setUp(self):
        self.datetime_example = '2019:12:29 21:44:22'
        self.file_name = 'IMG_4600.JPG'
        self.new_file_name_keep = '2019-12-29_21-44-22_IMG_4600.JPG'
        self.new_file_name_keep_not = '2019-12-29_21-44-22.JPG'

    def test_keep(self):
        self.assertEqual(self.new_file_name_keep,
                         pt.generateNewFileName(self.datetime_example, self.file_name, True))

    def test_not_keep(self):
        self.assertEqual(self.new_file_name_keep_not,
                         pt.generateNewFileName(self.datetime_example, self.file_name, False))


class TestGenerateNewPathsRelPath(unittest.TestCase):
    def setUp(self):
        self.source = 'test'
        self.target = 'test_renamed'
        self.input = [self.source + '/subdir/IMG_4600.JPG', self.source + '/fileWithoutExif.txt']

    def test_keep(self):
        correct_paths = [self.target + '/subdir/2019-12-29_21-44-22_IMG_4600.JPG',
                         self.target + '/fileWithoutExif.txt']
        correct_without_exif = [self.target + '/fileWithoutExif.txt']
        actual_paths, actual_without_exif = pt.generateNewPaths(self.input, self.source,
                                                                self.target, True)

        self.assertEqual(len(correct_paths), len(actual_paths))
        self.assertEqual(correct_paths.sort(), actual_paths.sort())

        self.assertEqual(len(correct_without_exif), len(actual_without_exif))
        self.assertEqual(correct_without_exif.sort(), actual_without_exif.sort())

    def test_keep_not(self):
        correct_paths = [self.target + '/subdir/2019-12-29_21-44-22.JPG',
                         self.target + '/fileWithoutExif.txt']
        correct_without_exif = [self.target + '/fileWithoutExif.txt']
        actual_paths, actual_without_exif = pt.generateNewPaths(self.input, self.source,
                                                                self.target, False)

        self.assertEqual(len(correct_paths), len(actual_paths))
        self.assertEqual(correct_paths.sort(), actual_paths.sort())

        self.assertEqual(len(correct_without_exif), len(actual_without_exif))
        self.assertEqual(correct_without_exif.sort(), actual_without_exif.sort())


class TestGenerateNewPathsAbsPath(unittest.TestCase):
    def setUp(self):
        self.source = os.getcwd() + '/test'
        self.target = os.getcwd() + '/out/test_renamed'
        self.input = [self.source + '/subdir/IMG_4600.JPG', self.source + '/fileWithoutExif.txt']

    def test_keep(self):
        correct_paths = [self.target + '/subdir/2019-12-29_21-44-22_IMG_4600.JPG',
                         self.target + '/fileWithoutExif.txt']
        correct_without_exif = [self.target + '/fileWithoutExif.txt']
        actual_paths, actual_without_exif = \
            pt.generateNewPaths(self.input, self.source, self.target, True)

        self.assertEqual(len(correct_paths), len(actual_paths))
        self.assertEqual(correct_paths.sort(), actual_paths.sort())

        self.assertEqual(len(correct_without_exif), len(actual_without_exif))
        self.assertEqual(correct_without_exif.sort(), actual_without_exif.sort())


if __name__ == '__main__':
    unittest.main()
