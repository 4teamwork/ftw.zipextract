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
        self.events = []
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
        self.events = []

    @adapter(IObjectAddedEvent)
    def handleAdded(self, event):
        self.events.append(event)

    @adapter(IObjectCreatedEvent)
    def handleCreated(self, event):
        self.events.append(event)

    @adapter(IObjectModifiedEvent)
    def handleModified(self, event):
        self.events.append(event)


class TestCreateObjectEventsAT(FunctionalTestCase):

    layer = FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_ATTypes
    expected_events = [
        ('ObjectCreatedEvent', u'multizip'),
        ('ObjectAddedEvent', u'multizip'),
        ('ContainerModifiedEvent', u'folder'),
        ('ObjectInitializedEvent', u'multizip'),
        ('ObjectCreatedEvent', 'test.txt'),
        ('ObjectAddedEvent', 'test.txt'),
        ('ContainerModifiedEvent', u'multizip'),
        ('ObjectInitializedEvent', 'test.txt'),
        ('ObjectCreatedEvent', u'dir1'),
        ('ObjectAddedEvent', u'dir1'),
        ('ContainerModifiedEvent', u'multizip'),
        ('ObjectInitializedEvent', u'dir1'),
        ('ObjectCreatedEvent', 'test3.txt'),
        ('ObjectAddedEvent', 'test3.txt'),
        ('ContainerModifiedEvent', u'dir1'),
        ('ObjectInitializedEvent', 'test3.txt'),
        ('ObjectCreatedEvent', 'test2.txt'),
        ('ObjectAddedEvent', 'test2.txt'),
        ('ContainerModifiedEvent', u'dir1'),
        ('ObjectInitializedEvent', 'test2.txt'),
        ('ObjectCreatedEvent', u'dir2'),
        ('ObjectAddedEvent', u'dir2'),
        ('ContainerModifiedEvent', u'dir1'),
        ('ObjectInitializedEvent', u'dir2'),
        ('ObjectCreatedEvent', 'test4.txt'),
        ('ObjectAddedEvent', 'test4.txt'),
        ('ContainerModifiedEvent', u'dir2'),
        ('ObjectInitializedEvent', 'test4.txt'),
    ]

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

        self.maxDiff = None
        self.assertEqual(
            self.expected_events,
            [(type(event).__name__, event.object.title)
              for event in self.eventCatcher.events])


class TestCreateObjectEventsDX(TestCreateObjectEventsAT):

    layer = FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_DXTypes
    expected_events =  [
        ('ObjectCreatedEvent', 'multi'),
        ('ObjectAddedEvent', 'multi'),
        ('ContainerModifiedEvent', u'folder'),
        ('ObjectCreatedEvent', 'test.txt'),
        ('ObjectAddedEvent', 'test.txt'),
        ('ContainerModifiedEvent', 'multi'),
        ('ObjectCreatedEvent', 'dir1'),
        ('ObjectAddedEvent', 'dir1'),
        ('ContainerModifiedEvent', 'multi'),
        ('ObjectCreatedEvent', 'test3.txt'),
        ('ObjectAddedEvent', 'test3.txt'),
        ('ContainerModifiedEvent', 'dir1'),
        ('ObjectCreatedEvent', 'test2.txt'),
        ('ObjectAddedEvent', 'test2.txt'),
        ('ContainerModifiedEvent', 'dir1'),
        ('ObjectCreatedEvent', 'dir2'),
        ('ObjectAddedEvent', 'dir2'),
        ('ContainerModifiedEvent', 'dir1'),
        ('ObjectCreatedEvent', 'test4.txt'),
        ('ObjectAddedEvent', 'test4.txt'),
        ('ContainerModifiedEvent', 'dir2'),
    ]
