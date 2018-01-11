from ftw.zipextract.implementations_base import ObjectCreatorBase
from ftw.zipextract.interfaces import IFileCreator
from ftw.zipextract.interfaces import IFolderCreator
from zope.component import adapts
from zope.interface import implements
from plone.app.contenttypes.interfaces import IFile
from plone.app.contenttypes.interfaces import IFolder


class DXFolderCreator(ObjectCreatorBase):
    implements(IFolderCreator)
    adapts(IFolder)
    portal_type = "Folder"


class DXFileCreator(ObjectCreatorBase):
    implements(IFileCreator)
    adapts(IFile)
    portal_type = "File"
