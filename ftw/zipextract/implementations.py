from ftw.zipextract.interfaces import IFileCreator
from ftw.zipextract.interfaces import IFolderCreator
from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.content.file import IATFile
from Products.ATContentTypes.content.folder import IATFolder

class ObjectCreatorBase():
    """
    Abstract base class for implementing the IFolderCreator interface
    """
    def __init__(self, context):
        self.context = context

    def create(self, folder, obj_id, name):
        folder.invokeFactory(type_name=self.portal_type, id=obj_id, title=name)

class ATFileCreator(ObjectCreatorBase):
    implements(IFileCreator)
    adapts(IATFile)
    portal_type = "File"

class ATFolderCreator(ObjectCreatorBase):
    implements(IFolderCreator)
    adapts(IATFolder)
    portal_type = "Folder"
