from fabric.api import local, run, cd, task, sudo


@task
def deploy():
    sudo("apt-get -q -y install subversion")


@task
def commit():
    from . import get_commit_message
    commit_message = get_commit_message()
    local("svn update && svn commit -m %s" % commit_message)


@task
def checkout(directory, scm_path):
    with cd(directory):
        local("svn co %s %s" % (scm_path, directory))


@task
def clone(directory):
    checkout(directory)


@task
def update(directory):
    with cd(directory):
        local("svn update")


@task
def pull(directory):
    update(directory)


@task
def remote_checkout(directory, scm_path):
    with cd(directory):
        run("svn co %s %s" % (scm_path, directory))


@task
def remote_clone(directory):
    remote_checkout(directory)


@task
def remote_update(directory):
    with cd(directory):
        run("svn update")


@task
def remote_pull(directory):
    remote_update(directory)
