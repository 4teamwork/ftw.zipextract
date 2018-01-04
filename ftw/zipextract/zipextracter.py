from AccessControl import Unauthorized
import os
from plone import api
from Products.CMFCore.interfaces import IFolderish
from plone.i18n.normalizer.interfaces import IIDNormalizer
from tempfile import NamedTemporaryFile
from ftw.zipextract.interfaces import IFolderCreator
from ftw.zipextract.interfaces import IFileCreator
from ftw.zipextract.interfaces import IFile
from ftw.zipextract import _
from ftw.zipextract import logger
import zipfile
from ZODB.POSException import ConflictError
from zope import component
try:
    from zope.app.container.interfaces import INameChooser
except ImportError:
    from zope.container.interfaces import INameChooser


class _FileNode():

    def __init__(self, parent_folder, filename, fileid, info):
        self.name = _(filename)
        self.info = info
        self.parent_folder = parent_folder
        self.id = fileid
        self.is_folder = False

    @property
    def path(self):
        return os.path.join(self.parent_folder.path, self.id)


class _FolderNode():

    def __init__(self, parent_folder, folder_name):
        self.name = folder_name
        self.subtree = {}
        self.file_dict = {}
        self.parent_folder = parent_folder
        self.id = self.name
        self.is_folder = True

    @property
    def path(self):
        if self.parent_folder:
            return os.path.join(self.parent_folder.path, self.id)
        else:
            return self.id

    def get_files(self):
        file_list = list(self.file_dict.values())
        for folder_node in self.subtree:
            file_list.extend(self.subtree[folder_node].get_files())
        return file_list


class ZipExtracter():
    """
    This should be initialized with a file object.
    It implements an "extract" method, which creates
    a new file object for every file in the zip, so
    it needs to extract that file and save it to disk,
    but also create the file object in zope
    """

    def __init__(self, context, max_size=None):
        file = IFile(context).get_blob()
        self.context = context
        self.parent_node = context.getParentNode()
        self.zfile = zipfile.ZipFile(file.open())
        self.file_name = os.path.basename(self.context.virtual_url_path())
        self.parent_folder = os.path.dirname(self.context.virtual_url_path())
        self.file_infos = self.extract_file_infos()
        self._extract_file_tree()
        self.max_size = max_size
        self.file_creator = IFileCreator(self.context)
        #self.folder_creator = IFolderCreator(self.parent_node)

    def _isdir(self, type):
        if type == "Folder":
            return True
        return False

    def extract_file_infos(self):
        return self.zfile.infolist()

    @staticmethod
    def generate_id(name, context):
        normalizer = component.getUtility(IIDNormalizer)
        chooser = INameChooser(context)
        normalized = normalizer.normalize(name)
        normalized = normalized.replace('_', '-').replace(' ', '-').lower()
        return chooser.chooseName(normalized, context)

    @staticmethod
    def generate_dict_key(name, d):
        name = os.path.splitext(name)[0]
        if not name in d:
            return name
        i = 1
        while True:
            new_name = name + "-{}".format(i)
            if new_name in d:
                i += 1
                continue
            return new_name

    def _extract_file_tree(self):
        self.file_tree = _FolderNode(None, "")
        # We first make all the directories
        for info in self.file_infos:
            is_folder = self.is_folder(info.filename)
            target_path = self.get_target_path(info)
            keys = target_path.split(os.path.sep)
            if not is_folder:
                keys = keys[:-1]
            curr_node = self.file_tree
            for k in keys:
                if not k in curr_node.subtree:
                    curr_node.subtree[k] = _FolderNode(curr_node, k)
                curr_node = curr_node.subtree[k]
        # Now we add the files
        for info in self.file_infos:
            is_folder = self.is_folder(info.filename)
            target_path = self.get_target_path(info)
            if is_folder:
                continue
            keys = target_path.split(os.path.sep)
            curr_node = self.file_tree
            for k in keys[:-1]:
                curr_node = curr_node.subtree[k]

            filename = keys[-1]
            file_id = self.generate_dict_key(filename, curr_node.file_dict)
            curr_node.file_dict[file_id] = _FileNode(
                curr_node, filename, file_id, info)

    def is_folder(self, path):
        if path.endswith("/"):
            return True
        else:
            return False

    def get_target_path(self, member):
        """ Build destination pathname, making it platform
        independent, and ensuring the path cannot point outside
        the current directory
        """
        arcname = member.filename.replace('/', os.path.sep)
        if os.path.altsep:
            arcname = arcname.replace(os.path.altsep, os.path.sep)
        arcname = os.path.splitdrive(arcname)[1]
        arcname = os.path.sep.join(x for x in arcname.split(os.path.sep)
                                   if x not in ('', os.path.curdir, os.path.pardir))
        if os.path.sep == '\\':
            # filter illegal characters on Windows
            illegal = ':<>|"?*'
            if isinstance(arcname, unicode):
                table = {ord(c): ord('_') for c in illegal}
            else:
                table = string.maketrans(illegal, '_' * len(illegal))
            arcname = arcname.translate(table)
            # remove trailing dots
            arcname = (x.rstrip('.') for x in arcname.split(os.path.sep))
            arcname = os.path.sep.join(x for x in arcname if x)
        return os.path.normpath(arcname)

    @staticmethod
    def check_path_inside_destination(targetpath, destinationpath):
        targetpath = os.path.join(destinationpath, targetpath)
        targetpath = os.path.normpath(targetpath)
        realpath = os.path.abspath(os.path.realpath(targetpath))
        if not realpath.startswith(os.path.abspath(destinationpath)):
            print("targetpath outside of destination directory. Skipping")
            return False
        return True

    @staticmethod
    def folder_exists(path):

        portal = api.portal.get()
        try:
            folder = portal.unrestrictedTraverse(path)
        except AttributeError:
            return False
        except KeyError:
            return False
        return IFolderish.providedBy(folder) and folder

    def create_object(self, extract_to, node):

        if node.parent_folder:
            base_path = os.path.join(extract_to, node.parent_folder.path)
        else:
            base_path = extract_to
        folder = self.folder_exists(base_path)
        if not folder:
            return None
        newid = self.generate_id(node.id, folder)
        node.id = newid
        error = ''
        try:
            #folder.invokeFactory(type_name=node.portal_type, id=newid, title=node.name)
            if node.is_folder:
                IFolderCreator(folder).create(folder, newid, node.name)
                #self.folder_creator.create(folder, newid, node.name)
            else:
                self.file_creator.create(folder, newid, node.name)

        except Unauthorized:
            error = u'serverErrorNoPermission'
        except ConflictError:
            # rare with xhr upload / happens sometimes with flashupload
            error = u'serverErrorZODBConflict'
        except Exception, e:
            error = u'serverError'
            logger.exception(e)
        if error:
            error = u'serverError'
            logger.info("An error happens with setId from filename, "
                        "the file has been created with a bad id, "
                        "can't find %s", newid)
        else:
            obj = getattr(folder, newid)
            return obj

    @staticmethod
    def copyfileobj(fsrc, fdst, max_size, buffer_length=16 * 1024):
        # copy data from file-like object fsrc to file-like object fdst
        tot_size = 0
        while tot_size <= max_size:
            buf = fsrc.read(buffer_length)
            if not buf:
                return tot_size
            fdst.write(buf)
            tot_size += len(buf)
        return None

    def create_parent_folders(self, extract_to, folder_node):
        parent_folder = folder_node.parent_folder
        if parent_folder and not self.folder_exists(os.path.join(extract_to, parent_folder.path)):
            self.create_parent_folders(extract_to, parent_folder)
        if not self.folder_exists(os.path.join(extract_to, folder_node.path)):
            self.create_object(extract_to, folder_node)

    def extract_file(self, file_node, extract_to=None):
        if extract_to == None:
            extract_to = self.parent_folder
        target_path = file_node.path
        if not self.check_path_inside_destination(target_path, extract_to):
            return
        self.create_parent_folders(extract_to, file_node.parent_folder)
        with self.zfile.open(file_node.info) as source, \
                NamedTemporaryFile(prefix="plone_zipextract_", delete=False) as target:
            written = self.copyfileobj(
                source, target, file_node.info.file_size)
            if not written == file_node.info.file_size:
                print("did not finish writing file")
                return file
            target.flush()
        file = self.create_object(extract_to, file_node)
        IFile(file).set_file(target, file_node.name)
        return file

    def extract(self, extract_to=None, create_root_folder=True, file_list=None):
        if extract_to == None:
            extract_to = self.parent_folder
        if not self.folder_exists(extract_to):
            print("folder does not exist")
            return
        if create_root_folder:
            self.file_tree.id = self.file_name
            self.file_tree.name = self.file_name
            folder = self.create_object(extract_to, self.file_tree)
        if file_list == None:
            file_list = self.file_tree.get_files()
        tot_size = sum([file.info.file_size for file in file_list])
        if self.max_size and tot_size > self.max_size:
            return
        for file_node in file_list:
            self.extract_file(file_node, extract_to)
