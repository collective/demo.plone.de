# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.layout.viewlets.common import ViewletBase


class DemoVersionViewlet(ViewletBase):
    """A Viewlets that show us the Plone Version."""

    index = ViewPageTemplateFile('templates/version_viewlet.pt')

    def get_plone_version(self):
        return api.env.plone_version()
