import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
debug = True
pid = "/srv/myapp/run/logger.pid"
errorlog = "/srv/myapp/logs/error.log"
proc_name = "myapp"
pythonpath = "/srv/myapp/app:/srv/myapp/lib/python2.7:/srv/myapp/scripts:/srv/myapp/lib/python2.7/site-packages"
bind = "unix:/srv/myapp/run/gunicorn.sock"
