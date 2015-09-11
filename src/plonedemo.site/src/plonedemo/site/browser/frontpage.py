# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class FrontPage(BrowserView):

    index = ViewPageTemplateFile('frontpage.pt')
