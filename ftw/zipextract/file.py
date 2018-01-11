from ftw.zipextract.interfaces import IFile
import mimetypes
from plone.namedfile.file import NamedBlobFile
from zope.interface import implements


class FileBase():
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

    def set_file(self):
        raise NotImplementedError()


class ATFile(FileBase):
    """ Adapter for archetype files
    """

    def get_content_type(self):
        return self.context.content_type

    def get_blob(self):
        return self.context.getFile().getBlob()

    def get_data(self):
        """ Only used for tests
        """
        return self.context.data

    def set_file(self, blob_file, filename):
        self.get_blob().consumeFile(blob_file.name)
        self.context.setFilename(filename)



class DXFile(FileBase):
    """ Adapter for archetype files
    """

    def get_content_type(self):
        # return self.context.content_type()
        return self.get_blob().contentType

    def get_blob(self):
        return self.context.file

    def get_data(self):
        """ Only used for tests
        """
        return self.get_blob().data

    def set_file(self, blob_file, filename):
        mimetype = mimetypes.guess_type(filename)[0]
        self.context.file = NamedBlobFile(
            data=open(blob_file.name),
            filename=filename,
            contentType=mimetype)
        self.context.reindexObject()
