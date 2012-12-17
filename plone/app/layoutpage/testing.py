from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class LayoutPageLayer(PloneSandboxLayer):

    defaultBases = PLONE_FIXTURE,

    def setUpZope(self, app, configurationContext):
        import plone.app.layoutpage
        self.loadZCML(package=plone.app.layoutpage)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.layoutpage:default')

        setRoles(portal, TEST_USER_ID, ['Manager', 'Member'])
        self['folder'] = portal[portal.invokeFactory(type_name='Folder',
                                id='foo-folder', title='Foo Folder')]
        setRoles(portal, TEST_USER_ID, ['Member'])

LAYOUT_PAGE_FIXTURE = LayoutPageLayer()
LAYOUT_PAGE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LAYOUT_PAGE_FIXTURE, ),
    name='LayoutPage:Integration')
LAYOUT_PAGE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LAYOUT_PAGE_FIXTURE, ),
    name='LayoutPage:Functional')
