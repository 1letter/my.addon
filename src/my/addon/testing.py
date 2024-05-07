from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing.zope import WSGI_SERVER_FIXTURE

import my.addon


class MyAddonLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=my.addon)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "my.addon:default")


MY_ADDON_FIXTURE = MyAddonLayer()


MY_ADDON_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MY_ADDON_FIXTURE,),
    name="MyAddonLayer:IntegrationTesting",
)


MY_ADDON_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MY_ADDON_FIXTURE,),
    name="MyAddonLayer:FunctionalTesting",
)


MY_ADDON_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MY_ADDON_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        WSGI_SERVER_FIXTURE,
    ),
    name="MyAddonLayer:AcceptanceTesting",
)
