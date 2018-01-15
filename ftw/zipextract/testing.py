from ftw.builder.content import register_at_content_builders
from ftw.builder.content import register_dx_content_builders
from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from zope.configuration import xmlconfig


class ModuleLayerATTypes(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'ftw.zipextract')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.zipextract:default')
        register_at_content_builders(force=True)


class ModuleLayerDXTypes(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        z2.installProduct(app, 'ftw.zipextract')
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')
        register_dx_content_builders(force=True)


MODULE_FIXTURE = ModuleLayerATTypes()
FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_ATTypes = FunctionalTesting(
    bases=(MODULE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.zipextract:functional_at")

MODULE_FIXTURE = ModuleLayerDXTypes()
FTW_ZIPEXTRACT_FUNCTIONAL_TESTING_DXTypes = FunctionalTesting(
    bases=(MODULE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.zipextract:functional_dx")
