from ftw.zipextract.testing import FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_ATTypes
from ftw.zipextract.tests import FunctionalTestCase
from Products.CMFCore.utils import getToolByName


class TestDefaultProfile(FunctionalTestCase):

    layer = FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_ATTypes

    def test_installed(self):
        portal_setup = getToolByName(self.portal, 'portal_setup')
        version = portal_setup.getLastVersionForProfile('ftw.zipextract:default')
        self.assertNotEqual(version, None)
        self.assertNotEqual(version, 'unknown')
