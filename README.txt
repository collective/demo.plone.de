==============
demo.plone.org
==============

This is the buildout and package used for demo.plone.org

Is uses the starzel-buildout (https://github.com/starzel/buildout)

Reset
=====

Todo: Docu Ansible plone.maintenance (ask @Gomez or @pbauer)

IP & Ports
==========

**demo.plone.org (Plone: lastest stable, Python: 3.11)**

- zeoclient1: 127.0.0.1:8082
- zeoclient2: 127.0.0.1:8083
- zeoserver:  127.0.0.1:8090

**classic.demo.plone.org (Plone: 6.0.x, Python: 3.11)**

- instance: 127.0.0.1:8072


Changes compared to stock-plone
===============================

Among other things the `setuphandler <https://github.com/collective/demo.plone.de/blob/master/src/plonedemo.site/src/plonedemo/site/setuphandlers.py>`_ of ``plonesite.demo`` loads two zexp-files into the site and links the content as translations.

The login-form is overriden with z3c.jbot to enable autologin with different roles. The users for that are created by the setuphandler.

Languages
=========

`plone.app.multilingual` is installed by default and demo-content is created in german, english, spanish and basque. Pull-request for additional languages are welcome but have to contain new zexp for the demo-content. See https://github.com/collective/demo.plone.de/pull/17 for an example.

We can add additional country-specific domains to the nginx-config.
