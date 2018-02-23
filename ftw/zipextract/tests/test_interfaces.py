from ftw.zipextract.factory_type_decider import DefaultFactoryTypeDecider
from ftw.zipextract.file import ATFile
from ftw.zipextract.file import DXFile
from ftw.zipextract.implementations_at import ATFileCreator
from ftw.zipextract.implementations_at import ATFolderCreator
from ftw.zipextract.implementations_dx import DXFileCreator
from ftw.zipextract.implementations_dx import DXFolderCreator
from ftw.zipextract.interfaces import IFactoryTypeDecider
from ftw.zipextract.interfaces import IFile
from ftw.zipextract.interfaces import IFileCreator
from ftw.zipextract.interfaces import IFolderCreator
from zope.interface.verify import verifyClass
import unittest


class InterfacesTests(unittest.TestCase):

    def test_ATFile_conforms_to_IFile(self):
        verifyClass(IFile, ATFile)

    def test_DXFile_conforms_to_IFile(self):
        verifyClass(IFile, DXFile)

    def test_DefaultFactoryTypeDecider_conforms_to_IFactoryTypeDecider(self):
        verifyClass(IFactoryTypeDecider, DefaultFactoryTypeDecider)

    def test_ATFileCreator_conforms_to_IFileCreator(self):
        verifyClass(IFileCreator, ATFileCreator)

    def test_ATFolderCreator_conforms_to_IFolderCreator(self):
        verifyClass(IFolderCreator, ATFolderCreator)

    def test_DXFileCreator_conforms_to_IFileCreator(self):
        verifyClass(IFileCreator, DXFileCreator)

    def test_DXFolderCreator_conforms_to_IFolderCreator(self):
        verifyClass(IFolderCreator, DXFolderCreator)
