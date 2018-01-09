#from opengever.document.document import IDocumentSchema
from zope.component import adapts
from zope.interface import implements
from interfaces import IFile


class _FileBase():
    implements(IFile)

    def __init__(self, context):
        self.context = context

    def _is_zip(self):
        return self.get_blob() and self.get_content_type() == 'application/zip'


class DocumentSchemaFile(_FileBase):

    def get_content_type(self):
        return self.context.content_type()

    def get_blob(self):
        return self.context.file

    def set_file(self, blob_file, filename):
        self.context.update_file(open(blob_file.name),
                                 "application/text", filename)

class FtwFile(_FileBase):

    def get_content_type(self):
        return self.context.content_type

    def get_blob(self):
        return self.context.getFile().getBlob()

    def set_file(self, blob_file, filename):
        self.get_blob().consumeFile(blob_file.name)
        self.context.setFilename(filename)
