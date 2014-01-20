#!/bin/bash

ROOTDIR=/srv/logger
APPDIR=${ROOTDIR}/app
SCRIPTSDIR=${ROOTDIR}/scripts

export PYTHONPATH=${APPDIR}:${ROOTDIR}/lib/python2.7:${ROOTDIR}/lib/python2.7/site-packages:${PYTHONPATH}:${SCRIPTSDIR}

source ${ROOTDIR}/bin/activate

exec ${ROOTDIR}/bin/gunicorn -c ${ROOTDIR}/conf/gunicorn-logger.py wsgi:app
