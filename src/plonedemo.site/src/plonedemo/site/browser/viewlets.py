# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from plone import api

class DemoVersionViewlet(ViewletBase):
    """A Viewlets that show us the Plone Version
    """

    index = ViewPageTemplateFile('templates/version_viewlet.pt')

    def get_plone_version(self):
        # Plone Version
        return api.env.plone_version()
