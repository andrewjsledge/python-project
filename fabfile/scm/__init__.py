import sys

__all__ = []
scm_path = None


def get_commit_message():
    print "Commit message (end with Ctrl-D): "
    commit_message = sys.stdout.read()
    return commit_message


def set_scm_path(path):
    global scm_path
    scm_path = path


def get_scm_path():
    return scm_path
