from Products.Five.browser import BrowserView
from ftw.zipextract.zipextracter import ZipExtracter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.i18n.normalizer import idnormalizer
import os
from z3c.form import form

class ZipExtractView(form.Form):

    template = ViewPageTemplateFile('templates/zipextract.pt')

    def __call__(self):
        self.zipextracter = ZipExtracter(self.context)
        self.build_tree_html()
        if self.request.get('form.submitted'):
            self.unzip(self.request)
            return self.redirect_to_workspace()
        return self.template()

    @staticmethod
    def _file_size_repr(file_node):
        size = file_node.info.file_size
        if size > 1024:
            return str(size/1024)+"KB"
        else:
            return str(size)+"B"

    def _recurse_tree_html(self, folder_node):
        for file_node in folder_node.file_dict.values():
            label = file_node.name + ": " + self._file_size_repr(file_node)
            self.tree_html += '<li id="{id}" class="file"><input type="checkbox" value="{path}"\
                id="{id}_checkbox" name="files:list" /><label for="{id}_checkbox">{name}</label></li>\n'\
                .format(path=file_node.path, name=label, id=idnormalizer.normalize(file_node.path))
        for key in folder_node.subtree:
            child_folder = folder_node.subtree[key]
            self.tree_html += '<li id="{id}" class="folder"><input type="checkbox" value="{path}"\
                id="{id}_checkbox" /><label for="{id}_checkbox">{name}</label><ul>\n'\
                .format(path=child_folder.path, name=child_folder.name, id=idnormalizer.normalize(child_folder.path))
#            self.tree_html += '<li id="{}">{}<ul>\n'.format(child_folder.path, key)
            self._recurse_tree_html(child_folder)
            self.tree_html += '</ul></li>'

    def build_tree_html(self):
        self.tree_html = '<ul class="zipextract file_tree" >\n'
        self._recurse_tree_html(self.zipextracter.file_tree)
        self.tree_html += '</ul>'

    def unzip(self, request):
        if not request.get('extract'):
            return
        if request.get('extract') == "Extract all":
            file_list=None
        elif request.get('files'):
            file_list = request.get('files')
            file_list = map(self.map_id_to_node, file_list)
        create_root = request.get("create root folder") and True or False
        self.zipextracter.extract(create_root_folder=create_root, file_list=file_list)
        return

    def map_id_to_node(self, node_id):
        keys = node_id.split(os.path.sep)
        node = self.zipextracter.file_tree
        for k in keys[:-1]:
            node = node.subtree[k]
        return node.file_dict[keys[-1]]

    def redirect_to_workspace(self):
        url = self.context.absolute_url()
        return self.request.RESPONSE.redirect(url)


