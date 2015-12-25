# -*- coding: utf-8 -*-
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.interfaces import ILanguage
from Products.CMFPlone.utils import bodyfinder
from plone import api
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone.app.multilingual.interfaces import ITranslationManager
from plone.app.textfield.value import RichTextValue
from plonedemo.site import _
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import implements
import logging
import os

logger = logging.getLogger(__name__)

DEFAULT_EMAIL = 'demo@plone.de'
TARGET_LANGUAGE = 'de'
FRONTPAGE_TITLE = _(u'Welcome to Plone 5')
FRONTPAGE_DESCRIPTION = _('The ultimate Open Source Enterprise CMS')


class HiddenProfiles(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'plondemo.site:uninstall',
        ]


def post_install(setup):
    """Post install script"""
    if setup.readDataFile('plonedemosite_default.txt') is None:
        return
    portal = api.portal.get()
    remove_content(portal)
    create_demo_users()
    languages = api.portal.get_registry_record('plone.available_languages')
    setupTool = SetupMultilingualSite()
    setupTool.setupSite(portal)
    for index, lang in enumerate(languages):
        container = portal[lang]
        frontpage = create_frontpage(
            portal, container=container, target_language=lang)
        container.setDefaultPage('frontpage')
        if index > 0:
            previous_lang = languages[index-1]
            previous_frontpage = portal[previous_lang]['frontpage']
            ITranslationManager(frontpage).register_translation(
                previous_lang, previous_frontpage)
        import_zexp(
            setup,
            filename='demo_%s.zexp' % lang,
            container=container,
            name='demo',
            update=True,
            publish=True,
        )


def uninstall(setup):
    """Uninstall script"""
    if setup.readDataFile('plonedemosite_uninstall.txt') is None:
        return
    # Do something during the uninstallation of this package


def remove_content(portal):
    default_content = [
        'front-page',
        'Members',
        'news',
        'events',
    ]
    for item in default_content:
        api.content.delete(portal[item])


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
         'roles': ('Reader', 'Reviewer', 'Editor', 'Member'),
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


def create_frontpage(portal, container, target_language):
    if not container.get('frontpage'):
        frontpage = api.content.create(
            container, 'Document', 'frontpage', FRONTPAGE_TITLE)
        api.content.transition(frontpage, to_state='published')
    frontpage = container.get('frontpage')
    front_text = None
    util = queryUtility(ITranslationDomain, 'plonedemo.site')
    frontpage.title = util.translate(FRONTPAGE_TITLE,
                                     target_language=target_language)
    frontpage.description = util.translate(FRONTPAGE_DESCRIPTION,
                                           target_language=target_language)

    if target_language != 'en':
        # get text from the translation-machinery
        translated_text = util.translate(
            _('plonedemo_frontpage'), target_language=target_language)
        if translated_text != u'plonedemo_frontpage':
            front_text = translated_text

    request = getattr(portal, 'REQUEST', None)
    if front_text is None and request is not None:
        # get text from rendering the template sice I cannot find a way to
        # return the default
        view = api.content.get_view('demo-frontpage', portal, request)
        front_text = bodyfinder(view.index()).strip()

    frontpage.text = RichTextValue(
        front_text,
        'text/html',
        'text/x-html-safe'
    )
    ILanguage(frontpage).set_language(target_language)
    return frontpage


def import_zexp(setup, filename, container, name, update=True, publish=True):
    """Import a zexp
    """
    # check if file is actually in profiles/default
    path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'profiles', 'default', filename)
    if filename not in setup.listDirectory(path=None):
        logger.info('zexp-file {0} does not exist'.format(path))
        return
    if name in container.keys():
        if not update:
            logger.info('Keeping {0}. Import of zexp aborted.'.format(name))
            return
        else:
            logger.info('Purging {0}.'.format(name))
            api.content.delete(container.get(name), check_linkintegrity=False)

    # Import zexp
    container._importObjectFromFile(str(path), verify=0)

    # publish all items!
    if publish:
        new = container[name]
        path = '/'.join(new.getPhysicalPath())
        catalog = api.portal.get_tool('portal_catalog')
        for brain in catalog(path={'query': path, 'depth': 2}):
            item = brain.getObject()
            try:
                api.content.transition(item, to_state='published')
            except WorkflowException:
                pass
