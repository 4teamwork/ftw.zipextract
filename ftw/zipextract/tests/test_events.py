from ftw.builder import Builder
from ftw.builder import create
from ftw.zipextract.testing import FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_ATTypes
from ftw.zipextract.testing import FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_DXTypes
from ftw.zipextract.tests import FunctionalTestCase
from ftw.zipextract.zipextracter import ZipExtracter
from zope.component import adapter
from zope.component import getSiteManager
from zope.component import provideHandler
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
import os


class EventCatcher(object):

    def __init__(self):
        self.added = []
        self.created = []
        self.modified = []
        self.setUp()

    def setUp(self):
        provideHandler(self.handleAdded)
        provideHandler(self.handleCreated)
        provideHandler(self.handleModified)

    def tearDown(self):
        getSiteManager().unregisterHandler(self.handleAdded)
        getSiteManager().unregisterHandler(self.handleCreated)
        getSiteManager().unregisterHandler(self.handleModified)

    def reset(self):
        self.added = []
        self.created = []
        self.modified = []

    @adapter(IObjectAddedEvent)
    def handleAdded(self, event):
        self.added.append(event)

    @adapter(IObjectCreatedEvent)
    def handleCreated(self, event):
        self.created.append(event)

    @adapter(IObjectModifiedEvent)
    def handleModified(self, event):
        self.modified.append(event)


class TestCreateObjectEventsAT(FunctionalTestCase):

    layer = FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_ATTypes
    added_titles = [u'multizip', 'test.txt', u'dir1', 'test3.txt',
                    'test2.txt', u'dir2', 'test4.txt']
    modified_titles = [u'folder', u'multizip', u'multizip',
                       u'dir1', u'dir1', u'dir1', u'dir2']

    def setUp(self):
        super(TestCreateObjectEventsAT, self).setUp()
        self.grant('Manager')
        self.folder = create(Builder('folder').titled(u'folder'))
        self.add_multi_zip_file()
        self.eventCatcher = EventCatcher()

    def tearDown(self):
        self.eventCatcher.tearDown()

    def add_multi_zip_file(self):
        """ This zip file contains 3 files and a directory
        """
        self.file = create(
            Builder('file')
            .titled(u'multizip')
            .attach_file_containing(self.asset('multi.zip'), u'multi.zip')
            .within(self.folder))

    def asset(self, filename):
        path = os.path.join(os.path.dirname(__file__), 'assets', filename)
        with open(path, 'r') as fh:
            return fh.read()

    def test_record_created_event_is_fired(self):
        extracter = ZipExtracter(self.file)
        extracter.extract()

        self.assertEqual(
            map(lambda x: x.object.title, self.eventCatcher.added),
            self.added_titles)

        self.assertEqual(
            map(lambda x: x.object.title, self.eventCatcher.created),
            self.added_titles)

        self.assertEqual(
            map(lambda x: x.object.title, self.eventCatcher.modified),
            self.modified_titles)


class TestCreateObjectEventsDX(TestCreateObjectEventsAT):

    layer = FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_DXTypes
    added_titles = [u'multi', 'test.txt', u'dir1', 'test3.txt',
                    'test2.txt', u'dir2', 'test4.txt']
    modified_titles = [u'folder', u'multi', u'multi',
                       u'dir1', u'dir1', u'dir1', u'dir2']
