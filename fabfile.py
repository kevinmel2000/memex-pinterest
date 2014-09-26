# -*- coding: utf-8 -*-
"""
To deploy updated changes to UI and Crawler code run

    fab push

It requires git to have a remote named 'prod'; to create it locally run

    fab setup_git

"""
from __future__ import absolute_import
import os
from fabric.api import local, run, cd, env, sudo, task, execute, warn_only

env.hosts = ["ubuntu@54.68.208.175"]

SYS_PACKAGES = [
    'python-dev',
    'python-lxml',
    'python-setuptools',
    'libssl-dev',
    'curl',
    'git',
    'libjpeg-dev',
    'build-essential',
    'python-scipy',
    'libxml2-dev',
    'libxslt-dev',
    'lib32z1-dev',
    'libffi-dev',  # for recent twisted

    'docker.io',  # it is 0.9, but that's fine

    # scipy deps
    'liblapack-dev',
    'libatlas-dev',
    'libsparskit-dev',
    'libarpack2-dev',
    'gfortran',
    'libfftw3-dev',
    'libblas-dev',
]

@task
def install_system_packages():
    """ Install required system packages """
    # sudo function doesn't work here - why?
    packages = ' '.join(SYS_PACKAGES)
    run('sudo apt-get install %s' % packages)


@task
def install_python_requirements():
    """ Install all Python-level requirements """
    with cd('hack1'):
        run('pip install --user -r ui/requirements.txt')
        run('pip install --user -r crawler/requirements.txt')


@task
def setup_git():
    """ Setup local git repo for pushing to production server """
    host = env.hosts[0]
    with warn_only():
        local('git remote rm prod')
    local('git remote add prod ssh://%s/~/hack1/' % host)


@task
def create_remote_repo():
    run('mkdir -p hack1')
    with cd('hack1'):
        run('git init')
        run('git config receive.denyCurrentBranch ignore')  # allow update current branch


@task
def git_push():
    local("git push prod")
    with cd("hack1"):
        run("git reset --hard master")


@task
def push():
    git_push()
    # TODO: restart flask?
