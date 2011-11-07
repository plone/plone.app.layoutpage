from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Layer(PloneSandboxLayer):
    
    defaultBases = (PLONE_FIXTURE,)
    
    def setUpZope(self, app, configurationContext):
        import plone.app.layoutpage
        self.loadZCML(package=plone.app.layoutpage)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.layoutpage:default')


FIXTURE = Layer()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='plone.app.layoutpage:Integration')
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name='plone.app.layoutpage:Functional')
