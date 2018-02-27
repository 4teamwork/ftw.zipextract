from ftw.zipextract.interfaces import IFactoryTypeDecider
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IFactoryTypeDecider)
@adapter(Interface, Interface)
class DefaultFactoryTypeDecider(object):

    folder_type = 'Folder'
    file_type = 'File'

    def __init__(self, container, request):
        self.container = container
        self.request = request

    def get_folder_fti(self, path, name):
        fti = getToolByName(self.container, 'portal_types').get(self.folder_type)
        return fti

    def get_file_fti(self, path, name, mimetype):
        fti = getToolByName(self.container, 'portal_types').get(self.file_type)
        return fti
