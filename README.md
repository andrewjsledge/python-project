python-project
==============

A boilerplate project for creating Python based projects. Requires
virtualenv and virtualenvwrapper.


Usage and Installation
======================

Add this to your postmkvirtualenv hook (i.e.: /home/andrew/.virtualenvs/postmkvirtualenv)

```shell

# Build from boilerplate
mv $VIRTUAL_ENV ${VIRTUAL_ENV}_
git clone https://github.com/andrewjsledge/python-project.git $VIRTUAL_ENV
mv $VIRTUAL_ENV ${VIRTUAL_ENV}__
mv ${VIRTUAL_ENV}_ $VIRTUAL_ENV
cp -R ${VIRTUAL_ENV}__/.git ${VIRTUAL_ENV}/.git
rm -rf ${VIRTUAL_ENV}__

cd $VIRTUAL_ENV && git reset --hard HEAD && git pull && cd -

mv ${VIRTUAL_ENV}/gitignore ${VIRTUAL_ENV}/.gitignore
mv ${VIRTUAL_ENV}/svnignore ${VIRTUAL_ENV}/.svnignore

pip install -r ${VIRTUAL_ENV}/requirements.txt

# Cleanup
rm -rf ${VIRTUAL_ENV}/.git

```

When you run ```mkvirtualenv <project name>```, it will clone this
repository and do a little bit extra work.
