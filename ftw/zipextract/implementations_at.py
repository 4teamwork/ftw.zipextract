from ftw.zipextract.interfaces import IFileCreator
from ftw.zipextract.interfaces import IFolderCreator
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope import component
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


try:
    from zope.app.container.interfaces import INameChooser
except ImportError:
    from zope.container.interfaces import INameChooser


def normalize_id(name):
    normalizer = component.getUtility(IIDNormalizer)
    normalized = normalizer.normalize(name)
    return normalized


@implementer(IFolderCreator)
@adapter(Interface, Interface, Interface)
class ATFolderCreator(object):

    def __init__(self, container, request, fti):
        self.container = container
        self.request = request
        self.fti = fti

    def create(self, name):
        normalized_id = normalize_id(name)
        chooser = INameChooser(self.container)
        new_id = chooser.chooseName(normalized_id, self.container)
        obj_id = self.container.invokeFactory(self.fti.id, new_id, title=name)
        obj = getattr(self.container, obj_id)
        obj.processForm()
        return obj


@implementer(IFileCreator)
@adapter(Interface, Interface, Interface)
class ATFileCreator(object):

    def __init__(self, container, request, fti):
        self.container = container
        self.request = request
        self.fti = fti

    def create(self, filename, temp_file, mimetype):
        normalized_id = normalize_id(filename)
        chooser = INameChooser(self.container)
        new_id = chooser.chooseName(normalized_id, self.container)
        obj_id = self.container.invokeFactory(self.fti.id, new_id, title=filename)
        obj = getattr(self.container, obj_id)
        file_wrapper = obj.getFile()
        file_wrapper.getBlob().consumeFile(temp_file.name)
        file_wrapper.setContentType(mimetype)
        file_wrapper.setFilename(filename)
        obj.processForm()
        return obj
