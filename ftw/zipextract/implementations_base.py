
class ObjectCreatorBase():
    """
    Abstract base class for implementing the IFolderCreator interface
    """
    def __init__(self, context):
        self.context = context

    def create(self, folder, obj_id, name):
        folder.invokeFactory(type_name=self.portal_type, id=obj_id, title=name)
