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
def demo_host(branch='master', latest=False, python3=False):
    """
    Host serving our Plone demo
    """
    env.hosts = ['demo.plone.de']
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
        with cd(env.directory):
            sudo('./bin/supervisorctl stop all', user=env.deploy_user)


def start():
    """
    Start up the Zope Instance
    """
    if env.latest and not env.python3:
        sudo('/bin/systemctl start demo-latest.service', shell=False)
    elif env.latest and env.python3:
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
        if env.latest and not env.python3:
            sudo('/bin/systemctl restart demo-latest.service', shell=False)
        elif env.latest and env.python3:
            sudo('/bin/systemctl restart demo-latest-py3.service', shell=False)
        else:
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
        sudo('ln -s local_production.cfg local.cfg', user=env.deploy_user)
        sudo('echo -e "[buildout]\nlogin = admin\npassword = admin" > secret.cfg', user=env.deploy_user)  # noqa: E501

        # bootstrap and run bildout once
        sudo('./bin/pip install -r requirements.txt', user=env.deploy_user)
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
        result = sudo('git pull', user=env.deploy_user)
        quick_update = 'Already up-to-date.' in result

    # Override quickupdate if we updating the latest sites
    if env.latest:
        quick_update = False

    if quick_update:
        # Plonesite Recipe replaces site on the fly
        print 'UPDATE: No full Buildout required: {0:s}'.format(result)
        # buildout
        stop()
        with cd(env.directory):
            sudo('./bin/buildout install plonesite', user=env.deploy_user)
        start()

    else:
        stop()
        with cd(env.directory):
            sudo('git checkout {}'.format(env.branch), user=env.deploy_user)

            # bootstrap

            if env.latest:
                sudo('./bin/pip install --no-cache-dir -r https://raw.githubusercontent.com/plone/buildout.coredev/5.2/requirements.txt', user=env.deploy_user)
                sudo('rm -rf ./src-mrd', user=env.deploy_user)
            else:
                sudo('./bin/pip install --no-cache-dir -r requirements.txt', user=env.deploy_user)

            sudo('rm -rf ./var/blobstorage', user=env.deploy_user)
            sudo('rm -rf ./var/filestorage', user=env.deploy_user)
            sudo('rm -f .installed.cfg', user=env.deploy_user)

            # buildout
            if env.latest and env.python3:
                sudo('./bin/buildout -c local_demo_latest_py3.cfg', user=env.deploy_user)
            else:
                sudo('./bin/buildout', user=env.deploy_user)

        # start zope
        start()
        # We Single ZEO on the nightly installations
        with cd(env.directory):
            if env.latest:
                sudo("sleep 15")
                sudo('./bin/instance adduser admin admin', user=env.deploy_user)  # noqa: E501

        if env.latest and env.python3:
            with cd(env.directory):
                sudo("sleep 15")
                sudo("/usr/bin/wget -O- --user=admin --password=admin --post-data='site_id=Plone&form.submitted=True&title=Website&default_language=de&portal_timezone=Europe/Berlin&extension_ids=plonetheme.barceloneta:default&extension_ids=plone.app.contenttypes:plone-content&extension_ids=plonedemo.site:default' http://127.0.0.1:6543/@@plone-addsite &> /dev/null", user=env.deploy_user)

        # load page twice to fill cache and prevent a bug showing raw html
        sudo('/usr/bin/wget -S -qO- demo.plone.de > /tmp/demo.plone.de.html', user=env.deploy_user)  # noqa: E501
        sudo('/usr/bin/wget -S -qO- demo.plone.de > /tmp/demo.plone.de.html', user=env.deploy_user)  # noqa: E501
