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
