# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from my.addon.testing import MY_ADDON_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that my.addon is properly installed."""

    layer = MY_ADDON_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if my.addon is installed."""
        self.assertTrue(self.installer.is_product_installed("my.addon"))

    def test_browserlayer(self):
        """Test that IMyAddonLayer is registered."""
        from my.addon.interfaces import IMyAddonLayer
        from plone.browserlayer import utils

        self.assertIn(IMyAddonLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MY_ADDON_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("my.addon")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if my.addon is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("my.addon"))

    def test_browserlayer_removed(self):
        """Test that IMyAddonLayer is removed."""
        from my.addon.interfaces import IMyAddonLayer
        from plone.browserlayer import utils

        self.assertNotIn(IMyAddonLayer, utils.registered_layers())
