from ftw.zipextract.zipextracter import ZipExtracter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
import os


class ZipExtractView(BrowserView):

    template = ViewPageTemplateFile('templates/zipextract.pt')

    def __call__(self):
        self.zipextracter = ZipExtracter(self.context)
        if self.request.get('form.submitted'):
            self.unzip(self.request)
            return self.redirect_to_container()
        return self.template()

    def filename(self):
        return os.path.basename(self.context.absolute_url_path())

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
        site_properties = getToolByName(self.context, 'portal_properties').site_properties
        if self.context.portal_type in site_properties.typesUseViewActionInListings:
            url += '/view'
        return self.request.RESPONSE.redirect(url)
