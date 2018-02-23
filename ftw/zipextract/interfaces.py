from zope.interface import Interface


class IFile(Interface):
    """The Ifile interface is used to standardise a few methods in file handling
    """

    def __init__(context):
        """Adapts a context, typically a file object
        """

    def is_zip():
        """True if it is a zip file
        """

    def get_blob():
        """Returns the associated blob file
        """


class IFolderCreator(Interface):
    """The folder creator is used to create a folder in
    a given container
    """

    def __init__(container, request, fti):
        """The folder creator is a multi adapter of container
        request and factory type information
        """

    def create(name):
        """creates a folder named 'name' in the container
        """


class IFileCreator(Interface):
    """The folder creator is used to create a file in
    a given container
    """

    def __init__(container, request, fti):
        """The file creator is a multi adapter of container
        request and factory type information
        """

    def create(filename, temp_file, mimetype):
        """creates a file named 'filename' in the container, storing the data
        from temp_file (a tempfile.NamedTemporaryFile)
        """


class IFactoryTypeDecider(Interface):
    """The factory type decider decides which factory type information
    to use for creating folders or files from the zip within a specific
    container.
    """

    def __init__(container, request):
        """The factory type decider is a multi adapter of container and request.
        """

    def get_folder_fti(path, name):
        """returns an FTI from the path to the container and name of the folder
        to be created
        """

    def get_file_fti(path, name, mimetype):
        """returns an FTI from the path to the container and name of the file
        to be created
        """
