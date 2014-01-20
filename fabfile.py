import sys

from fabric.api import local, run, env

SCM = "git"
SOURCE_DIRECTORY = "/home/andrew/work/applications/python-project-boilerplate/src"

#### VM SETUP


def setup_development():
    development_setup()
    env.host = '192.168.99.99'
    env.user = 'andrew'
    env.password = 'alpha'


#### HOST SETUP


def development_setup():
    env.host = '192.168.99.99'
    env.user = 'vagrant'
    env.password = 'vagrant'

    if run("who | grep andrew").failed:
        run("useradd -d /home/andrew -g admin -G sudo -p alpha andrew")
        local("ssh-copy-id 192.168.99.99")


#### COMMIT


def get_commit_message():
    print "Enter the commit message. Control-D to quit:"
    commit_message = sys.stdin.read()
    return commit_message


def git_commit():
    commit_message = get_commit_message()
    local("git add -p && git commit -m %s" % commit_message)


def svn_commit():
    commit_message = get_commit_message()
    local("svn update && svn commit -m %s" % commit_message)


def commit():
    if SCM is "git":
        git_commit()
    elif SCM is "svn":
        svn_commit()


#### PUSH
