HOSTS = {'development':
         {'ip': '192.168.99.99',
          'user': 'vagrant',
          'password': 'vagrant',
          'packages': ("nginx", "python-dev", "python-pip",
                       "supervisor", "libpq-dev", "subversion",
                       "postgresql-server-dev-all"),
          'python_packages': ("virtualenv", "virtualenvwrapper"),
          },
         'staging':
         {'ip': '192.168.99.100',
          'user': 'andrew',
          'password': 'password',
          'packages': ("nginx", "python-dev", "python-pip",
                       "supervisor", "libpq-dev", "subversion",
                       "postgresql-server-dev-all"),
          'python_packages': ("virtualenv", "virtualenvwrapper"),
          },
         'production':
         {'ip': '192.168.99.200',
          'user': 'andrew',
          'password': 'password',
          'packages': ("nginx", "python-dev", "python-pip",
                       "supervisor", "libpq-dev", "subversion",
                       "postgresql-server-dev-all"),
          'python_packages': ("virtualenv", "virtualenvwrapper"),
          }
         }


APPS = {'myapp':
        {'scm_path': "https://github.com/andrewjsledge/python-project.git",
         'scm_user': "andrewjsledge",
         'scm_type': "git",
         'src_dir': "/home/andrew/work/applications/myapp",
         'deploy_dir': "/srv/myapp",
         'python_packages': ("gunicorn", "setproctitle",
                             "flask-restless", "sqlalchemy",
                             "flask-sqlalchemy", "flask-login",
                             "flask-openid", "flask-wtf",
                             "wtforms", "dateutils", "psycopg2"),
         'configs_dir': "conf",
         'logs_dir': "logs",
         'tmp_dir': "tmp",
         'run_dir': "run",
         'requirements_file': "conf/requirements.txt"}
        }
