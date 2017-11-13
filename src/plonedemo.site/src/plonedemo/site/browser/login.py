# -*- coding: utf-8 -*-
from plone.login.interfaces import ILoginForm
from plone.z3cform.templates import FormTemplateFactory
from plonedemo.site.interfaces import IPlonedemoSiteLayer

import os


# Override login form template
loginform_templatefactory = FormTemplateFactory(
    os.path.join(os.path.dirname(__file__), 'templates/login.pt'),
    form=ILoginForm,
    request=IPlonedemoSiteLayer,
    )
