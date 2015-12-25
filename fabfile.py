# -*- coding: utf-8 -*-
"""
Fabric script to manage demo
"""

from fabric.api import env, cd, sudo, run
from fabric.decorators import task

# Fabric uses the ~/.ssh/config 
# Needed here because of wrong dns
env.use_ssh_config = True

@task
def demo_host(branch='master'):
    """
    Host serving our Plone demo
    """
    env.hosts = ['demo.plone.de']
    env.port = '30363'
    env.deploy_user = 'zope'
    env.branch = branch
    env.homedir = '/home/%s/' % env.deploy_user
    env.directory = '/home/%s/demo.plone.de/' % env.deploy_user


def stop():
    """
    Shutdown the Zope Instance
    """
    with cd(env.directory):
        sudo('./bin/supervisorctl stop all', user=env.deploy_user)


def start():
    """
    Start up the Zope Instance
    """
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
        sudo('git clone https://github.com/collective/demo.plone.de.git', user=env.deploy_user)


    with cd(env.directory):

        # requirements
        # sudo('python python-dev build-essential zlib1g-dev libssl-dev libxml2-dev libxslt1-dev wv poppler-utils libtiff5-dev libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev libwebp-dev')

        # prepare buildout
        sudo('ln -s local_production.cfg local.cfg', user=env.deploy_user)
        sudo('echo -e "[buildout]\nlogin = admin\npassword = admin" > secret.cfg', user=env.deploy_user)
        
        # bootstrap and run bildout once
        sudo('python bootstrap.py', user=env.deploy_user)
        sudo('./bin/buildout', user=env.deploy_user)

        # start supervisor which starts plone instance also
        sudo('./bin/supervisord', user=env.deploy_user)


@task
def update():
    """
    Update the instance and reinstall the demo
    """
    with cd(env.directory):
        
        # stop running plone
        stop()
        
        # update plone
        sudo('git pull', user=env.deploy_user)
        sudo('git checkout {}'.format(env.branch), user=env.deploy_user)
        
        # bootstrap
        sudo('python bootstrap.py', user=env.deploy_user)
        
        # delete database and sone files
        sudo('rm -rf .installed.cfg', user=env.deploy_user)
        sudo('rm -rf ./var/blobstorage', user=env.deploy_user)
        sudo('rm -rf ./var/filestorage', user=env.deploy_user)        

        # buildout
        sudo('./bin/buildout', user=env.deploy_user)
        
        # start zope
        start()