from StringIO import StringIO
from fabric.api import sudo, local, get, task
from fabric.contrib.files import append, exists


__all__ = ['user_add', 'user_remove', 'group_add', 'group_remove',
           'user_group_add', 'user_group_remove']


# Assumptions
#
# All accounts will have an associated group that will be created when
# the account is created.
#
# Using native Ubuntu/Debian utilities.


def get_max_system_user_id():
    if exists("/etc/max_system_user_id"):
        fd = StringIO()
        get("/etc/max_system_user_id", fd)
        max_id = fd.getvalue()
        return max_id
    return None


def put_max_system_user_id(i):
    sudo("echo %s > /etc/max_system_user_id" % i)


def create_system_user(username):
    i = get_max_system_user_id()
    if not i:
        i = "9000"
    else:
        temp_i = int(i) + 1
        i = str(temp_i)
    sudo("addgroup --system --gid %s %s" % (i, username))
    G = "adduser --system --no-create-home --disabled-password " + \
        "--disabled-login --uid %s --gid %s %s" % (i, i, username)
    put_max_system_user_id(i)
    sudo(G)


def create_regular_user(host, username):
    sudo("adduser --home /home/%s --gecos '' --shell "
         "/bin/bash %s" % (username, username))
    sudo("usermod -a -G %s,admin %s" % (username, username))
    local("ssh-copy-id %s" % host)


def create_user_virtualenv(username):
    venv_1 = "export WORKON_HOME=$HOME/.virtualenvs"
    venv_2 = "export PROJECT_HOME=/srv"
    venv_3 = "export " + \
        "VIRTUALENVWRAPPER_SCRIPT=/usr/local/bin/virtualenvwrapper.sh"
    venv_4 = "source /usr/local/bin/virtualenvwrapper_lazy.sh"
    append("/home/%s/.bashrc" % username, venv_1, use_sudo=True)
    append("/home/%s/.bashrc" % username, venv_2, use_sudo=True)
    append("/home/%s/.bashrc" % username, venv_3, use_sudo=True)
    append("/home/%s/.bashrc" % username, venv_4, use_sudo=True)


def get_users_current_groups(username):
    groups = sudo("groups %s" % username)
    groups = groups.split(" : ")[1]
    groups = groups.split(" ")
    return groups


@task
def user_add(host, username, usertype=None):
    if not usertype or usertype == "regular":
        create_regular_user(host, username)
        create_user_virtualenv(username)
    elif usertype == "system":
        create_system_user(username)


@task
def user_remove(username):
    sudo("deluser %s" % username)
    if exists("/home/%s" % username):
        sudo("rm -rf /home/%s" % username)


@task
def group_add(group):
    sudo("addgroup %s" % group)


@task
def group_remove(group):
    sudo("delgroup %s" % group)


@task
def user_group_add(username, group):
    groups = ",".join(get_users_current_groups(username))
    sudo("usermod -G %s,%s %s" % (groups, group, username))


@task
def user_group_remove(username, group):
    current_groups = get_users_current_groups(username)
    groups = current_groups.replace(group, "")
    new_groups = ",".join(groups)
    sudo("usermod -G %s %s" % (new_groups, username))
