from ftw.zipextract.interfaces import IFactoryTypeDecider
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

    def get_folder_portal_type(self, path, name):
        return self.folder_type

    def get_file_portal_type(self, path, name, mimetype):
        return self.file_type
