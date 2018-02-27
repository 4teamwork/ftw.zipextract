from ftw.zipextract.interfaces import IFile
from zope.interface import implements


class FileBase(object):
    """
    Abstract base class for implementing the IFIle interface.
    Should not be used on its own.
    """

    implements(IFile)

    def __init__(self, context):
        self.context = context

    def is_zip(self):
        return self.get_blob() and self.get_content_type() == 'application/zip'

    def get_content_type(self):
        raise NotImplementedError()

    def get_blob(self):
        raise NotImplementedError()


class ATFile(FileBase):
    """Adapter for archetype files
    """

    def get_content_type(self):
        return self.context.content_type

    def get_blob(self):
        return self.context.getFile().getBlob()

    def get_data(self):
        """Only used for tests
        """
        return self.context.data


class DXFile(FileBase):
    """Adapter for archetype files
    """

    def get_content_type(self):
        return self.get_blob().contentType

    def get_blob(self):
        return self.context.file

    def get_data(self):
        """Only used for tests
        """
        return self.get_blob().data
