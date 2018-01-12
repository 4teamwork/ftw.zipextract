from Products.Five.browser import BrowserView
from ftw.zipextract.zipextracter import ZipExtracter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.i18n.normalizer import idnormalizer
import os
from z3c.form import form


class ZipExtractView(form.Form):

    template = ViewPageTemplateFile('templates/zipextract.pt')

    def render(self):
        return self.template()

    def update(self):
        self.zipextracter = ZipExtracter(self.context)
        if self.request.get('form.submitted'):
            self.unzip(self.request)
            return self.redirect_to_container()

    @staticmethod
    def _file_size_repr(file_node):
        size = file_node.info.file_size
        if size > 1024:
            return str(size / 1024) + "KB"
        else:
            return str(size) + "B"

    def file_repr(self, file_node):
        return file_node.name + ": " + self._file_size_repr(file_node)

    @staticmethod
    def norm_id(node):
        return idnormalizer.normalize(node.path)

    def unzip(self, request):
        if not (request.get('extract all') or request.get("extract selected")):
            return
        file_list = None
        if request.get('extract selected'):
            file_list = request.get('files')
            if not file_list:
                return
            file_list = map(self.map_id_to_node, file_list)
        create_root = request.get("create root folder") and True or False
        self.zipextracter.extract(
            create_root_folder=create_root, file_list=file_list)
        return

    def map_id_to_node(self, node_id):
        keys = node_id.split(os.path.sep)
        node = self.zipextracter.file_tree
        for k in keys[:-1]:
            node = node.subtree[k]
        return node.file_dict[keys[-1]]

    def redirect_to_container(self):
        url = self.context.absolute_url()
        return self.request.RESPONSE.redirect(url)
