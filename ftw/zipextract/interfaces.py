from zope.interface import Interface


class IFile(Interface):
    pass


class IFolderCreator(Interface):
    pass


class IFileCreator(Interface):
    pass


class IFactoryTypeDecider(Interface):
    """The factory type decider decides which portal types to use for creating
    folders or files from the zip within a specific container.
    """

    def __init__(container, request):
        """The factory type decider is a multi adapter of container and request.
        """

    def get_folder_portal_type(path, name):
        """
        """

    def get_file_portal_type(path, name, mimetype):
        """
        """
