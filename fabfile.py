import sys

from fabric.api import local

SCM = "git"


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
