from ftw.builder import Builder
from ftw.builder import create
from ftw.testbrowser import browsing
from ftw.zipextract.interfaces import IFile
from ftw.zipextract.testing import FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_DXTypes
from ftw.zipextract.testing import FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_ATTypes
from ftw.zipextract.tests import FunctionalTestCase
from ftw.zipextract.zipextracter import ZipExtracter
from operator import itemgetter
from operator import methodcaller
import os
from unittest2 import TestCase


class ZipExtracterTestBase(FunctionalTestCase):

    def AddMultiZipFile(self):
        """ This zip file contains 3 files and a directory
        """
        self.file = create(
            Builder('file')
            .titled(u'multizip')
            .attach_file_containing(self.asset('multi.zip'), u'multi.zip')
            .within(self.folder))

    def AddOutsideZipFile(self):
        """ This zip contains a file "../test.txt"
        """
        self.file = create(
            Builder('file')
            .titled(u'outside')
            .attach_file_containing(self.asset('outside.zip'), u'outside.zip')
            .within(self.folder))

    def AddFalseSizeZipFile(self):
        """ This zip contains a file "test.txt" with a file size
        larger than announced in the header
        """
        self.file = create(
            Builder('file')
            .titled(u'false_size')
            .attach_file_containing(self.asset('false_size.zip'), u'false_size.zip')
            .within(self.folder))

    def AddTextFile(self):
        """ This zip file contains 3 files and a directory
        """
        self.file = create(
            Builder('file')
            .titled(u'text')
            .attach_file_containing(self.asset('test.txt'), u'test.txt')
            .within(self.folder))

    def asset(self, filename):
        path = os.path.join(os.path.dirname(__file__), 'assets', filename)
        with open(path, 'r') as fh:
            return fh.read()


class TestZipExtracterArchetype(ZipExtracterTestBase):

    layer = FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_ATTypes
    expected_titles = ['multizip', 'test3.txt', 'test.txt', 'test2.txt']
    expected_paths = ['/plone/folder/multizip', '/plone/folder/multizip-1/test3',
                      '/plone/folder/multizip-1/dir1/test', '/plone/folder/multizip-1/dir1/test2']
    traverse_error = AttributeError

    def setUp(self):
        super(TestZipExtracterArchetype, self).setUp()
        self.grant('Contributor')
        self.folder = create(Builder('folder').titled(u'folder'))

    def test_zipextracter_file_tree(self):
        self.AddMultiZipFile()
        extracter = ZipExtracter(self.file)
        tree = extracter.file_tree
        # Directory tree
        self.assertEqual(["dir1"], tree.subtree.keys())
        self.assertEqual([], tree.subtree["dir1"].subtree.keys())
        # Files
        self.assertEqual(["test3"], tree.file_dict.keys())
        self.assertEqual(["test", "test2"], tree.subtree[
                         "dir1"].file_dict.keys())
        self.assertEqual(["test3.txt", "test.txt", "test2.txt"], [
                         el.name for el in tree.get_files()])
        # Paths
        self.assertEqual(tree.subtree["dir1"].path, "dir1")
        self.assertEqual(tree.subtree["dir1"].file_dict[
                         "test"].path, "dir1/test")
        # folders are properly recognized
        self.assertEqual(tree.is_folder, True)
        self.assertEqual(tree.subtree["dir1"].is_folder, True)
        self.assertEqual(tree.file_dict["test3"].is_folder, False)

    def test_path_control(self):
        self.assertTrue(
            ZipExtracter.check_path_inside_destination("test/../../dir", "dir"))
        self.assertFalse(
            ZipExtracter.check_path_inside_destination("test/../../dir", ""))
        self.assertFalse(
            ZipExtracter.check_path_inside_destination("/test", ""))

    def test_zipextracter_extract_file_works(self):
        self.AddMultiZipFile()
        extracter = ZipExtracter(self.file)
        to_extract = extracter.file_tree.subtree["dir1"].file_dict["test"]
        with self.assertRaises(self.traverse_error):
            self.portal.unrestrictedTraverse("/plone/folder/dir1/test")
        extracter.extract_file(to_extract)
        file = self.portal.unrestrictedTraverse("/plone/folder/dir1/test")
        self.assertEqual(IFile(file).get_data(), 'This is a test text file')

    def test_zip_extract_all_works(self):
        self.AddMultiZipFile()
        extracter = ZipExtracter(self.file)
        extracter.extract()
        files = self.portal.portal_catalog(portal_type="File")
        self.assertEquals(4, len(files))
        titles = map(itemgetter("Title"), files)
        self.assertEquals(self.expected_titles, titles)
        paths = map(methodcaller("getPath"), files)
        self.assertEquals(self.expected_paths, paths)

    def test_handle_extract_outside_destination(self):
        self.AddOutsideZipFile()
        extracter = ZipExtracter(self.file)
        extracter.extract(create_root_folder=False)
        file = self.portal.portal_catalog(portal_type="File", Title="test")[0]
        self.assertEquals("/plone/folder/test", file.getPath())

    def test_handle_false_file_size(self):
        self.AddFalseSizeZipFile()
        extracter = ZipExtracter(self.file)
        nfiles = len(self.portal.portal_catalog(portal_type="File"))
        with self.assertRaises(IOError):
            extracter.extract()
        self.assertEquals(
            nfiles, len(self.portal.portal_catalog(portal_type="File")))

    @browsing
    def test_zip_extraction_view_works(self, browser):
        self.AddMultiZipFile()
        browser.visit(self.file, view="zipextract")
        file_tree = browser.css(".zipextract.file_tree li")
        id_list = map(lambda el: el.node.get("id"), file_tree)
        expected_ids = ['test3', 'dir1', 'dir1-test', 'dir1-test2']
        self.assertEquals(expected_ids, id_list)

    @browsing
    def test_zip_extraction_view_only_allowed_for_zip_files(self, browser):
        browser.exception_bubbling = True
        self.AddTextFile()
        with self.assertRaises(TypeError):
            browser.visit(self.file, view="zipextract")


class TestZipExtracterDexterity(TestZipExtracterArchetype):

    layer = FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_DXTypes
    expected_titles = ['multizip', 'test3.txt', 'test.txt', 'test2.txt']
    expected_paths = ['/plone/folder/multi.zip', '/plone/folder/multi-zip/test3',
                      '/plone/folder/multi-zip/dir1/test', '/plone/folder/multi-zip/dir1/test2']
    traverse_error = KeyError

    def setUp(self):
        super(TestZipExtracterArchetype, self).setUp()
        self.grant('Contributor')
        self.folder = create(Builder('folder').titled(u'folder'))
