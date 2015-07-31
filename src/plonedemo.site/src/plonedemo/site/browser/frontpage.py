from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView


class FrontPage(BrowserView):

    index = ViewPageTemplateFile('frontpage.pt')
