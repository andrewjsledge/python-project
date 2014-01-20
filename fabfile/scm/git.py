from fabric.api import local, run, cd, task, sudo

from . import scm_path


@task
def deploy():
    sudo("apt-get -q -y install git")


@task
def commit():
    from . import get_commit_message
    commit_message = get_commit_message()
    local("git add -p && git commit -m %s" % commit_message)


@task
def clone(directory):
    with cd(directory):
        local("git clone %s" % scm_path)


@task
def checkout(directory):
    clone(directory)


@task
def pull(directory):
    with cd(directory):
        local("git pull")


@task
def update(directory):
    pull(directory)


@task
def remote_clone(directory):
    with cd(directory):
        run("git clone %s" % scm_path)


@task
def remote_checkout(directory):
    remote_clone(directory)


@task
def remote_pull(directory):
    with cd(directory):
        run("git pull")


@task
def remote_update(directory):
    remote_pull(directory)
