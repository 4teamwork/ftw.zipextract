from ftw.zipextract.implementations_base import ObjectCreatorBase
from ftw.zipextract.interfaces import IFileCreator
from ftw.zipextract.interfaces import IFolderCreator
from zope.component import adapts
from zope.interface import implements
from Products.ATContentTypes.content.file import IATFile
from Products.ATContentTypes.content.folder import IATFolder


class ATFileCreator(ObjectCreatorBase):
    implements(IFileCreator)
    adapts(IATFile)
    portal_type = "File"


class ATFolderCreator(ObjectCreatorBase):
    implements(IFolderCreator)
    adapts(IATFolder)
    portal_type = "Folder"
