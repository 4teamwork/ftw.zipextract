#from opengever.document.document import IDocumentSchema
from zope.interface import implements
from ftw.zipextract.interfaces import IFile


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

    def set_file(self, blob_file, filename):
        self.get_blob().consumeFile(blob_file.name)
        self.context.setFilename(filename)
