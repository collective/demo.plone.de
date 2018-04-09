# -*- coding: utf-8 -*-
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.navigation.interfaces import INavigationRoot
from pkg_resources import get_distribution


class FrontpageViewlet(ViewletBase):
    """The frontpage as a viewlet."""

    def show(self):
        context_state = api.content.get_view(
            'plone_context_state', self.context, self.request)
        if INavigationRoot.providedBy(context_state.canonical_object()):
            return context_state.is_view_template()

    def get_plone_version(self):
        return get_distribution('Plone').version
