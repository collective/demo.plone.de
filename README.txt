====================
demo.plone.de
====================

This is a legacy project used to deploy 52.demo.plone.org

The new setup for https://demo.plone.org and https://classic.demo.plone.org is https://github.com/plone/demo.plone.org


Reset
=====

Todo: Docu Ansible plone.maintenance (ask @Gomez or @pbauer)

IP & Ports
==========

**52.demo.plone.de (Plone: lastest stable, Python: 3.7)**

- zeoclient1: 127.0.0.1:8082
- zeoclient2: 127.0.0.1:8083
- zeoserver:  127.0.0.1:8090


Languages
=========

`plone.app.multilingual` is installed by default and demo-content is created in german, english, spanish and basque. Pull-request for additional languages are welcome but have to contain new zexp for the demo-content. See https://github.com/collective/demo.plone.de/pull/17 for an example.

We can add additional country-specific domains to the nginx-config.
