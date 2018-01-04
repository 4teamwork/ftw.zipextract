from zope.interface import Interface


class IZip(Interface):
    """ Marker interface for Zip files
    """
    pass


class IFile(Interface):
    pass


class IFolderCreator(Interface):
    pass


class IFileCreator(Interface):
    pass


class ObjectCreatorBase():

    def __init__(self, context):
        self.context = context

    def create(self, folder, obj_id, name):
        folder.invokeFactory(type_name=self.portal_type, id=obj_id, title=name)
