# -*- coding: utf-8 -*-
from plone import api

DEFAULT_EMAIL = 'demo@plone.de'


def post_install(context):
    """Post install script"""
    if context.readDataFile('plonedemosite_default.txt') is None:
        return
    # Do something during the installation of this package
    demo_users = [
        {'login': 'reader',
         'password': 'reader',
         'fullname': 'Reader',
         'roles': ('Reader', ),
         },
        {'login': 'contributor',
         'password': 'contributor',
         'fullname': 'Contributor',
         'roles': ('Contributor', ),
         },
        {'login': 'editor',
         'password': 'editor',
         'fullname': 'Editor',
         'roles': ('Editor', ),
         },
        {'login': 'reviewer',
         'password': 'reviewer',
         'fullname': 'Reviewer',
         'groups': ['Reviewers'],
         'roles': ('Reviewer', ),
         },
        {'login': 'siteadmin',
         'password': 'siteadmin',
         'fullname': 'Site Admininstrator',
         'groups': ['Site Administrators'],
         'roles': ('Site Administrator', ),
         },
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


def uninstall(context):
    """Uninstall script"""
    if context.readDataFile('plonedemosite_uninstall.txt') is None:
        return
    # Do something during the uninstallation of this package
