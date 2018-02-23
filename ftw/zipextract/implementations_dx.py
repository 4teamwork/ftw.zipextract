from ftw.zipextract.interfaces import IFileCreator
from ftw.zipextract.interfaces import IFolderCreator
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import createContentInContainer
from plone.rfc822.interfaces import IPrimaryFieldInfo
from plone.namedfile.file import NamedBlobFile


@implementer(IFolderCreator)
@adapter(Interface, Interface, IDexterityFTI)
class DXFolderCreator(object):

    def __init__(self, container, request, fti):
        self.container = container
        self.request = request
        self.fti = fti

    def create(self, name):
        return createContentInContainer(self.container, self.fti.factory, title=name)


@implementer(IFileCreator)
@adapter(Interface, Interface, IDexterityFTI)
class DXFileCreator(object):

    def __init__(self, container, request, fti):
        self.container = container
        self.request = request
        self.fti = fti

    def create(self, filename, temp_file, mimetype):
        obj = createContentInContainer(self.container, self.fti.factory, id=filename, title=filename)
        field = IPrimaryFieldInfo(obj).field
        blob_file = NamedBlobFile(data=open(temp_file.name), filename=unicode(filename), contentType=mimetype)
        field.set(obj, blob_file)
        self.container.reindexObject()
        return obj
