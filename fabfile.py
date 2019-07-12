# -*- coding: utf-8 -*-
"""
Fabric script to manage demo
"""

from fabric.api import env, cd, sudo
from fabric.decorators import task

# Fabric uses the ~/.ssh/config
# Needed here because of wrong dns
env.use_ssh_config = True


@task
def demo_host(branch='master', latest=False, python3=True):
    """
    Host serving our Plone demo
    """
    env.hosts = ['demo.plone.de']
    env.domain = 'http://demo.plone.org'
    env.zeoclient_port = '8082'
    env.port = '30363'
    env.deploy_user = 'zope'
    env.branch = branch
    env.latest = latest
    env.python3 = python3
    env.homedir = '/home/%s/' % env.deploy_user
    env.directory = '/home/%s/demo.plone.de/' % env.deploy_user


@task
def demo_host_latest(branch='master', latest=True, python3=False):
    """
    Host serving our Plone demo
    """
    env.hosts = ['demo.plone.de']
    env.domain = 'http://demo-latest-py2.plone.org'
    env.zeoclient_port = '8072'
    env.port = '30363'
    env.deploy_user = 'zope'
    env.branch = branch
    env.latest = latest
    env.python3 = python3
    env.homedir = '/home/%s/' % env.deploy_user
    env.directory = '/home/%s/demo-latest.plone.de/' % env.deploy_user


@task
def demo_host_latest_py3(branch='master', latest=True, python3=True):
    """
    Host serving our Plone demo
    """
    env.hosts = ['demo.plone.de']
    env.domain = 'http://demo-latest-py3.plone.org'
    env.zeoclient_port = '8073'
    env.port = '30363'
    env.deploy_user = 'zope'
    env.branch = branch
    env.latest = latest
    env.python3 = python3
    env.homedir = '/home/%s/' % env.deploy_user
    env.directory = '/home/%s/demo-latest-py3.plone.de/' % env.deploy_user


def stop():
    """
    Shutdown the Zope Instance
    """
    if env.latest and not env.python3:
        sudo('/bin/systemctl stop demo-latest.service', shell=False)
    elif env.latest and env.python3:
        sudo('/bin/systemctl stop demo-latest-py3', shell=False)
    else:
        # demo site is multi instance, cant do supervisor for now
        with cd(env.directory):
            sudo('./bin/supervisorctl stop all', user=env.deploy_user)


def start():
    """
    Start up the Zope Instance
    """
    if env.latest:
        if env.python3:
            sudo('/bin/systemctl start demo-latest.service', shell=False)
        else:
            sudo('/bin/systemctl start demo-latest-py3', shell=False)
    else:
        with cd(env.directory):
            sudo('./bin/supervisorctl start all', user=env.deploy_user)


@task
def restart():
    """
    Restart the Zope Instance
    """
    with cd(env.directory):
        sudo('./bin/supervisorctl restart all', user=env.deploy_user)


@task
def setup():
    """
    Setup a newly installed vm
    """

    with cd(env.homedir):

        # clone repository from github
        sudo('git clone https://github.com/collective/demo.plone.de.git', user=env.deploy_user)  # noqa: E501

    with cd(env.directory):

        # requirements
        # sudo('python python-dev build-essential zlib1g-dev libssl-dev libxml2-dev libxslt1-dev wv poppler-utils libtiff5-dev libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev libwebp-dev')   # noqa: E501

        # prepare buildout
        if env.latest:
            if env.python3:
                sudo('ln -s local_demo_nightly_py3.cfg local.cfg', user=env.deploy_user)  # noqa: E501
            else:
                sudo('ln -s local_demo_nightly_py2.cfg local.cfg', user=env.deploy_user)  # noqa: E501
        else:
            sudo('ln -s local_production.cfg local.cfg', user=env.deploy_user)
        sudo('echo -e "[buildout]\nlogin = admin\npassword = admin" > secret.cfg', user=env.deploy_user)  # noqa: E501

        # bootstrap and run bildout once
        if env.latest:
            sudo('./bin/pip install --no-cache-dir -r https://raw.githubusercontent.com/plone/buildout.coredev/5.2/requirements.txt', user=env.deploy_user)  # noqa: E501
        else:
            sudo('./bin/pip install --no-cache-dir -r requirements.txt', user=env.deploy_user)  # noqa: E501
        sudo('./bin/buildout', user=env.deploy_user)

        # start supervisor which starts plone instance also
        sudo('./bin/supervisord', user=env.deploy_user)


@task
def update():
    """
    Update the instance and reinstall the demo
    """

    # update plone
    with cd(env.directory):
        sudo('git pull', user=env.deploy_user)

    with cd(env.directory):
        stop()
        sudo('git checkout {}'.format(env.branch), user=env.deploy_user)

        # bootstrap

        if env.latest:
            sudo('./bin/pip install --no-cache-dir -r https://raw.githubusercontent.com/plone/buildout.coredev/5.2/requirements.txt', user=env.deploy_user)  # noqa: E501
            sudo('rm -rf ./src-mrd', user=env.deploy_user)
        else:
            sudo('./bin/pip install --no-cache-dir -r requirements.txt', user=env.deploy_user)  # noqa: E501

        sudo('rm -rf ./var/blobstorage ./var/filestorage .installed.cfg ', user=env.deploy_user)  # noqa: E501

        # buildout
        sudo('./bin/buildout', user=env.deploy_user)

        # start zope
        start()

        # create plonesite with addons (uses different ports for py2 and py3)
        if env.latest:
            if env.python3:
                with cd(env.directory):
                    sudo("sleep 30")
                    sudo("/usr/bin/wget -O- --user=admin --password=admin --post-data='site_id=Plone&form.submitted=True&title=Website&default_language=de&portal_timezone=Europe/Berlin&extension_ids=plonetheme.barceloneta:default&extension_ids=plone.app.contenttypes:plone-content&extension_ids=plonedemo.site:default' http://127.0.0.1:{zeoclient_port}/@@plone-addsite &> ./var/log/wget_demo-plone-latest-py3.log".format(zeoclient_port=env.zeoclient_port), user=env.deploy_user)  # noqa: E501
            else:
                with cd(env.directory):
                    sudo("sleep 30")
                    sudo("/usr/bin/wget -O- --user=admin --password=admin --post-data='site_id=Plone&form.submitted=True&title=Website&default_language=de&portal_timezone=Europe/Berlin&extension_ids=plonetheme.barceloneta:default&extension_ids=plone.app.contenttypes:plone-content&extension_ids=plonedemo.site:default' http://127.0.0.1:{zeoclient_port}/@@plone-addsite &> ./var/log/wget_demo-plone-latest-py2.log".format(zeoclient_port=env.zeoclient_port), user=env.deploy_user)  # noqa: E501
        else:
            with cd(env.directory):
                sudo("sleep 50")
                sudo("/usr/bin/wget -O- --user=admin --password=admin --post-data='site_id=Plone&form.submitted=True&title=Website&default_language=de&portal_timezone=Europe/Berlin&extension_ids=plonetheme.barceloneta:default&extension_ids=plone.app.contenttypes:plone-content&extension_ids=plonedemo.site:default' http://127.0.0.1:{zeoclient_port}/@@plone-addsite &> ./var/log/wget_demo-plone.log".format(zeoclient_port=env.zeoclient_port), user=env.deploy_user)  # noqa: E501

        # load page to warmup
        sudo('/usr/bin/wget -S -qO- {domain} > /dev/null'.format(domain=env.domain), user=env.deploy_user)  # noqa: E501
