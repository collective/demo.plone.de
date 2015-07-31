# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import bodyfinder
from plone import api
from plone.app.textfield.value import RichTextValue
from plonedemo.site import _
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implements


DEFAULT_EMAIL = 'demo@plone.de'
TARGET_LANGUAGE = 'de'
FRONTPAGE_TITLE = _(u'Herzlich willkommen auf der Plone 5 Demo Website!')
FRONTPAGE_DESCRIPTION = _(u'Plone ist ein Open Source Content Management System, das Organisationen, Unternehmen und Privatanwendern die professionelle Erstellung und Verwaltung von Webseiten und Intranets ermöglicht.')  # noqa


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        """
        Prevents all profiles but 'plone-content' from showing up in the
        profile list when creating a Plone site.
        """
        return [
            u'plondemo.site:uninstall',
        ]


def post_install(context):
    """Post install script"""
    if context.readDataFile('plonedemosite_default.txt') is None:
        return
    portal = api.portal.get()
    create_demo_users()
    modify_frontpage(portal, TARGET_LANGUAGE)


def uninstall(context):
    """Uninstall script"""
    if context.readDataFile('plonedemosite_uninstall.txt') is None:
        return
    # Do something during the uninstallation of this package


def create_demo_users():
    # Do something during the installation of this package
    demo_users = [
        # {'login': 'reader',
        #  'password': 'reader',
        #  'fullname': 'Reader',
        #  'roles': ('Reader', ),
        #  },
        # {'login': 'contributor',
        #  'password': 'contributor',
        #  'fullname': 'Contributor',
        #  'roles': ('Contributor', ),
        #  },
        {'login': 'editor',
         'password': 'editor',
         'fullname': 'Editor',
         'roles': ('Reader', 'Contributor', 'Editor', 'Member'),
         },
        {'login': 'reviewer',
         'password': 'reviewer',
         'fullname': 'Reviewer',
         'groups': ['Reviewers'],
         'roles': ('Reviewer', ),
         },
        # {'login': 'siteadmin',
        #  'password': 'siteadmin',
        #  'fullname': 'Site Admininstrator',
        #  'groups': ['Site Administrators'],
        #  'roles': ('Site Administrator', ),
        #  },
        {'login': 'manager',
         'password': 'manager',
         'fullname': 'Manager',
         'groups': ['Administrators'],
         'roles': ('Administrator', ),
         },
    ]
    for demo_user in demo_users:
        if api.user.get(username=demo_user.get('login')):
            continue
        new_user = api.user.create(
            email=DEFAULT_EMAIL,
            username=demo_user.get('login'),
            password=demo_user.get('password'),
            roles=demo_user.get('roles'),
            properties={'fullname': demo_user.get('fullname')},
        )
        for group in demo_user.get('groups', []):
            api.group.add_user(
                groupname=group,
                user=new_user,
            )


def modify_frontpage(portal, target_language):
    frontpage = portal.get('front-page')
    if frontpage:
        api.content.rename(frontpage, 'frontpage')
    frontpage = portal.get('frontpage')
    front_text = None
    if target_language != 'en':
        util = queryUtility(ITranslationDomain, 'plonedemo.site')
        if util is not None:
            translated_text = util.translate(
                u'plonedemo-frontpage',
                target_language=target_language)
            if translated_text != u'plonedemo-frontpage':
                front_text = translated_text
    request = getattr(portal, 'REQUEST', None)
    if front_text is None and request is not None:
        view = api.content.get_view('demo-frontpage', portal, request)
        if view is not None:
            front_text = bodyfinder(view.index()).strip()
    frontpage.title = FRONTPAGE_TITLE
    frontpage.description = FRONTPAGE_DESCRIPTION
    frontpage.text = RichTextValue(
        front_text,
        'text/html',
        'text/x-html-safe'
    )
