import sys
import os

from fabric.api import sudo, hosts, env, task, run, cd
from fabric.contrib.files import exists

from . import config, users, application

PROD = config.HOSTS['production']['ip']
USER = config.HOSTS['production']['user']
PASSWD = config.HOSTS['production']['password']
HOST_PKGS = config.HOSTS['production']['packages']
PY_PKGS = config.HOSTS['production']['python_packages']


@task
@hosts(PROD)
def apt_install(pkg):
    apt_update()
    sudo("apt-get -q -y install %s" % pkg)


@task
@hosts(PROD)
def apt_upgrade_all():
    apt_update()
    sudo("apt-get -q -y upgrade")


@task
@hosts(PROD)
def apt_upgrade(pkg):
    #: Really, just for convenience
    apt_install(pkg)


@task
@hosts(PROD)
def apt_remove(pkg):
    sudo("apt-get -q -y remove %s" % pkg)


@task
@hosts(PROD)
def apt_update():
    sudo("apt-get -q update")


@task
@hosts(PROD)
def pip_install(pkg):
    sudo("pip install %s" % pkg)


@task
@hosts(PROD)
def pip_remove(pkg):
    sudo("pip uninstall %s" % pkg)


@task
@hosts(PROD)
def pip_upgrade(pkg):
    sudo("pip install --upgrade %s" % pkg)


@task
@hosts(PROD)
def reboot():
    sudo("shutdown -r now")


@task
@hosts(PROD)
def uptime():
    run("uptime")


@task
@hosts(PROD)
def who():
    run("who")


@task
@hosts(PROD)
def bootstrap():
    env.user = USER
    if PASSWD:
        env.password = PASSWD

    if not exists("/etc/machine_deployed"):
        host_installs = " ".join(HOST_PKGS)
        apt_install(host_installs)

        py_installs = " ".join(PY_PKGS)
        pip_install(py_installs)

        users.user_add(PROD, "webapp", "system")
        users.user_add(PROD, "andrew")

        users.user_group_add("andrew", "webapp")
        users.user_group_add("www-data", "webapp")
        sudo("touch /etc/machine_deployed")


@task
@hosts(PROD)
def clean():
    env.user = USER
    if PASSWD:
        env.password = PASSWD
    env.warn_only = True

    users.user_remove("andrew")
    users.user_remove("webapp")
    users.group_remove("andrew")
    users.group_remove("webapp")
    sudo("rm -rf /etc/machine_deployed")


@task
@hosts(PROD)
def app_bootstrap(app=None, user=None):
    if not app or not user:
        print 'app and user are required'
        sys.exit()

    env.warn_only = True

    deploy_dir = config.APPS[app]['deploy_dir']
    configs_dir = config.APPS[app]['configs_dir']
    logs_dir = config.APPS[app]['logs_dir']
    tmp_dir = config.APPS[app]['tmp_dir']
    scm_type = config.APPS[app]['scm_type']
    scm_path = config.APPS[app]['scm_path']
    python_pkgs = config.APPS[app]['python_packages']
    requirements_file = config.APPS[app]['requirements_file']

    conf_root = deploy_dir + os.sep + configs_dir
    log_root = deploy_dir + os.sep + logs_dir
    run_root = deploy_dir + os.sep + "run"
    bin_root = deploy_dir + os.sep + "bin"
    script_root = deploy_dir + os.sep + "scripts"
    nginx_conf = conf_root + os.sep + "nginx-" + app
    supervisor_conf = conf_root + os.sep + "supervisor-" + app

    sudo("mkdir -p %s" % deploy_dir)
    sudo("chmod -R 0775 %s" % deploy_dir)
    sudo("chown -R webapp:webapp %s" % deploy_dir)

    sudo("mkdir -p %s" % tmp_dir)
    sudo("chmod -R 0664 %s" % tmp_dir)
    sudo("umask 033 %s" % tmp_dir)
    sudo("chown -R webapp:webapp %s" % tmp_dir)

    py_installs = " ".join(python_pkgs)
    application.create_virtualenv(deploy_dir, user, py_installs)

    # virtualenv
    remote_update, remote_checkout = application.scm_funcs(scm_type)
    with cd(deploy_dir):
        remote_checkout(deploy_dir, scm_path)

    # requirements file
    if requirements_file:
        reqs_file = deploy_dir + os.sep + requirements_file
        if exists(reqs_file):
            application.pip_install_2_virtualenv(deploy_dir,
                                                 reqs_file_path=reqs_file)

    # log directories
    if not exists(log_root):
        sudo("mkdir -p %s" % log_root)

    # run directories
    if not exists(run_root):
        sudo("mkdir -p %s" % run_root)

    # gunicorn
    startup_script = bin_root + os.sep + "gunicorn_start.sh"
    if not exists(startup_script):
        sudo("mv %s/gunicorn_start.sh %s" %
             (script_root, startup_script))

    # nginx
    if exists(nginx_conf):
        sudo("cp %s /etc/nginx/sites-available/%s" % (nginx_conf, app))
        sudo("ln -s /etc/nginx/sites-available/%s "
             "/etc/nginx/sites-enabled/%s" % (app, app))

    # supervisor
    if exists(supervisor_conf):
        sudo("cp %s /etc/supervisor/conf.d/%s.conf" % (supervisor_conf, app))

    # secure and clean up
    application.finalize(deploy_dir, system_user="webapp")

    # start it up!
    sudo("supervisorctl reread")
    sudo("supervisorctl update")
    sudo("supervisorctl start logger")


@task
@hosts(PROD)
def app_clean(app):
    env.warn_only = True

    deploy_dir = config.APPS[app]['deploy_dir']

    sudo("rm -rf %s" % deploy_dir)
    if exists("/etc/nginx/sites-enabled/%s" % app):
        sudo("rm /etc/nginx/sites-enabled/%s" % app)
    if exists("/etc/nginx/sites-available/%s" % app):
        sudo("rm /etc/nginx/sites-available/%s" % app)
    if exists("/etc/supervisor/conf.d/%s.conf" % app):
        sudo("rm /etc/supervisor/conf.d/%s.conf" % app)

    sudo("supervisorctl reread")
    sudo("supervisorctl update")
    sudo("service supervisor stop")
    sudo("service supervisor start")
