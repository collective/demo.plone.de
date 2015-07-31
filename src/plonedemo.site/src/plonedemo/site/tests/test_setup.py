# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plonedemo.site.testing import PLONEDEMO_SITE_INTEGRATION_TESTING  # noqa
from plone import api

import unittest2 as unittest


class TestSetup(unittest.TestCase):
    """Test that plonedemo.site is properly installed."""

    layer = PLONEDEMO_SITE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if plonedemo.site is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('plonedemo.site'))

    def test_browserlayer(self):
        """Test that IPlonedemoSiteLayer is registered."""
        from plonedemo.site.interfaces import IPlonedemoSiteLayer
        from plone.browserlayer import utils
        self.assertIn(IPlonedemoSiteLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = PLONEDEMO_SITE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['plonedemo.site'])

    def test_product_uninstalled(self):
        """Test if plonedemo.site is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('plonedemo.site'))

    def test_browserlayer_removed(self):
        """Test that IPlonedemoSiteLayer is removed."""
        from plonedemo.site.interfaces import IPlonedemoSiteLayer
        from plone.browserlayer import utils
        self.assertNotIn(IPlonedemoSiteLayer, utils.registered_layers())
