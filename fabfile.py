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
def demo(branch='master'):
    """
    Demo Instance
    """
    env.hosts = ['demo.operun.de']
    env.port = '30363'
    env.deploy_user = 'zope'
    env.branch = branch
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
    Clone buildout and setup plone
    """
    with cd(env.directory):
        
        # stop running plone
        stop()
        
        # update plone
        update()        
        
        # bootstrap
        sudo('python bootstrap.py', user=env.deploy_user)
        
        # delete .installed.cfg to get correct admin user from buildout's secret.cfg
                
        # remove blobs
        sudo('rm -rf ./var/blobstorage', user=env.deploy_user)
        
        # remove database
        sudo('rm -rf ./var/filestorage', user=env.deploy_user)        

        # buildout
        sudo('./bin/buildout', user=env.deploy_user)
        
        # start zope
        start()


def update():
    """
    Update packages
    """
    with cd(env.directory):
        sudo('git pull', user=env.deploy_user)
        sudo('git checkout {}'.format(env.branch), user=env.deploy_user)


def buildout():
    """
    Run buildout
    """
    with cd(env.directory):
        sudo('./bin/buildout', user=env.deploy_user)


def deploy():
    """
    Deploy current status of development
    """
    update()
    buildout()
    restart()
