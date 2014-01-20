import sys

from fabric.api import sudo


def scm_funcs(scm_type):
    if scm_type == "svn":
        from scm.svn import remote_update, remote_checkout
    elif scm_type == "git":
        from scm.git import remote_update, remote_checkout
    return remote_update, remote_checkout


def pip_install_2_virtualenv(path, pkgs=None, reqs_file_path=None):
    # sudo("source %s/bin/activate" % path)
    if pkgs:
        sudo("pip install -E %s %s" % (path, pkgs))
    if reqs_file_path:
        sudo("pip install -E %s -r %s" % (path, reqs_file_path))


def create_virtualenv(path, user, python_pkgs):
    sudo("virtualenv %s" % path)
    pip_install_2_virtualenv(path, pkgs=python_pkgs)


def finalize(path, system_user=None):
    if not system_user:
        print 'No system user defined'
        sys.exit()
    sudo("chmod -R 0775 %s" % path)
    sudo("chown -R %s:%s %s" % (system_user, system_user, path))
