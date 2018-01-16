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
from plone.namedfile.file import NamedBlobFile
import mimetypes

def normalize_id(name):
    normalizer = component.getUtility(IIDNormalizer)
    normalized = normalizer.normalize(name)
    #normalized = normalized.replace('_', '-').replace(' ', '-').lower()
    return normalized

@implementer(IFolderCreator)
@adapter(Interface, Interface, Interface)
class ATFolderCreator(object):

    def __init__(self, container, request, fti):
        self.container = container
        self.request = request
        self.fti = fti

    def create(self, title):
        normalized_id = normalize_id(title)
        chooser = INameChooser(self.container)
        new_id = chooser.chooseName(normalized_id, self.container)
        #return self.container.invokeFactory(self.fti.factory, new_id, title=title)
        obj = self.container.invokeFactory("Folder", new_id, title=title)
        obj = getattr(self.container, obj)
        return obj


@implementer(IFileCreator)
@adapter(Interface, Interface, Interface)
class ATFileCreator(object):

    def __init__(self, container, request, fti):
        self.container = container
        self.request = request
        self.fti = fti

    def create(self, filename, temp_file):
        normalized_id = normalize_id(filename)
        chooser = INameChooser(self.container)
        new_id = chooser.chooseName(normalized_id, self.container)
        #obj = self.container.invokeFactory(self.fti.factory, new_id, title=filename)
        obj = self.container.invokeFactory("File", new_id, title=filename)
        mimetype = mimetypes.guess_type(filename)[0]
        #blob_file = NamedBlobFile(data=open(temp_file.name),filename=unicode(filename),contentType=mimetype)
        obj = getattr(self.container, obj)
        #obj.getPrimaryField().set(obj, blob_file)
        #field.set(obj, NamedBlobFile(blob_file))
        obj.getFile().getBlob().consumeFile(temp_file.name)
        return obj



