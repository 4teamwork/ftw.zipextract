from ftw.zipextract.interfaces import IFile
from plone import api
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
        data = self.get_data()
        mimetypes_registry = api.portal.get_tool('mimetypes_registry')
        mimetype = mimetypes_registry.classify(data, filename=self.get_filename())
        return mimetype and mimetype == mimetypes_registry.lookup('application/zip')[0]

    def get_filename(self):
        raise NotImplementedError()

    def get_content_type(self):
        raise NotImplementedError()

    def get_blob(self):
        raise NotImplementedError()

    def get_data(self):
        raise NotImplementedError()


class ATFile(FileBase):
    """Adapter for archetype files
    """

    def get_filename(self):
        return self.context.getFilename()

    def get_content_type(self):
        return self.context.content_type

    def get_blob(self):
        return self.context.getFile().getBlob()

    def get_data(self):
        return self.context.data


class DXFile(FileBase):
    """Adapter for archetype files
    """

    def get_filename(self):
        blob = self.get_blob()
        return blob.filename if blob else None

    def get_content_type(self):
        return self.get_blob().contentType

    def get_blob(self):
        return self.context.file

    def get_data(self):
        blob = self.get_blob()
        return blob.data if blob else None
