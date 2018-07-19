# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.navigation.interfaces import INavigationRoot

import pkg_resources


class FrontpageViewlet(ViewletBase):
    """The frontpage as a viewlet."""

    def show(self):
        context_state = api.content.get_view(
            'plone_context_state', self.context, self.request)
        if INavigationRoot.providedBy(context_state.canonical_object()):
            return context_state.is_view_template()

    def get_plone_version(self):
        try:
            return pkg_resources.get_distribution('Plone').version
        except pkg_resources.DistributionNotFound:
            return pkg_resources.get_distribution('Products.CMFPlone').version
