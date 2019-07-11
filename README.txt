====================
demo.plone.de
====================

This is the buildout and package used for demo.plone.de

Is uses the starzel-buildout (https://github.com/starzel/buildout)

Reset
=====

On california (KVM host) is a cron (/etc/cron.d/update_demo_plone_de) to execute fabric and reset the page every four hours.

.. code-block:: cron

    SHELL=/bin/sh
    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
    MAILTO=bofh@tcs.ifi.lmu.de
    # cron.daily/update_demo_plone_de -- daily reset of demo site
    0 0,4,8,12,16,20 * * *  root    /usr/local/bin/fab -f /root/demo.plone.de/fabfile demo_host update >>/var/log/demo.plone 2>&1

On budapest (KVM guest) /home/zope/ runs the plone sites

When this repository has no changes fabric only runs ``./bin/buildout install plonesite`` to speed up things. Otherwise it runs the complete buildout.

The sites are created with a `wget` that installs the profile ``plonedemo.site:default`` which creates some demo-content:

.. code-block:: shell

    /usr/bin/wget -O- --user=admin --password=admin --post-data='site_id=Plone&form.submitted=True&title=Website&default_language=de&portal_timezone=Europe/Berlin&extension_ids=plonetheme.barceloneta:default&extension_ids=plone.app.contenttypes:plone-content&extension_ids=plonedemo.site:default' http://127.0.0.1:8080/@@plone-addsite


systemd start/stop
==================

For the python 3 instance we use systemd to start/stop the process, here is the config file ``/etc/systemd/system/demo-latest-py3.service``. Useful commands are ``systemctl restart demo-latest-py3.service`` & ``systemctl status demo-latest-py3.service``

IP & Ports
==========

**demo.plone.de (Plone: lastest stable, Python: 3.7)**

- zeoclient1: 127.0.0.1:8082
- zeoclient2: 127.0.0.1:8083
- zeoserver:  127.0.0.1:8090

**demo-latest.plone.de (Plone: 5.2, Python: 2.7)**

- instance: 127.0.0.1:8072

**demo-latest-py3.plone.de (Plone: 5.2, Python 3.6)**

- instance: 127.0.0.1:8062

Changes compared to stock-plone
===============================

Among other things the `setuphandler <https://github.com/collective/demo.plone.de/blob/master/src/plonedemo.site/src/plonedemo/site/setuphandlers.py>`_ of ``plonesite.demo`` loads two zexp-files into the site and links the content as translations.

The login-form is overrriden with z3c.jbot to enable autologin with different roles. The users for that are created by the setuphandler.

Languages
=========

`plone.app.multilingual` is installed by default and demo-content is created in german, english, spanish and basque. Pull-request for additional languages are welcome but have to contain new zexp for the demo-content. See https://github.com/collective/demo.plone.de/pull/17 for an example.

We can add additional country-specific domains to the nginx-config.
