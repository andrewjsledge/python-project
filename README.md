python-project
==============

A boilerplate project for creating Python based projects. Requires
virtualenv and virtualenvwrapper.


Usage and Installation
======================

Add this to your postmkvirtualenv hook (i.e.: /home/andrew/.virtualenvs/postmkvirtualenv)

```shell

#!/bin/bash
# This hook is run after a new virtualenv is activated.

# Build from boilerplate

echo "Downloading boilerplate project"

mv $VIRTUAL_ENV ${VIRTUAL_ENV}_
git clone https://github.com/andrewjsledge/python-project.git $VIRTUAL_ENV
mv $VIRTUAL_ENV ${VIRTUAL_ENV}__
mv ${VIRTUAL_ENV}_ $VIRTUAL_ENV
cp -R ${VIRTUAL_ENV}__/.git ${VIRTUAL_ENV}/.git
rm -rf ${VIRTUAL_ENV}__

cd $VIRTUAL_ENV && git reset --hard HEAD && git pull && cd -
rm -rf ${VIRTUAL_ENV}/.git

echo "Setting up VCS settings"

mv ${VIRTUAL_ENV}/gitignore ${VIRTUAL_ENV}/.gitignore
mv ${VIRTUAL_ENV}/svnignore ${VIRTUAL_ENV}/.svnignore

echo "Installing packages"

pip install -q -r ${VIRTUAL_ENV}/requirements.txt

echo "Building virtual development machine"
# shut down any existing machine
vagrant halt
BNAME=`basename $VIRTUAL_ENV`
cd ${VIRTUAL_ENV}/vm && vagrant init ${BNAME}-precise32 http://files.vagrantup.com/precise32.box && vagrant up && cd -

# clean up Vagrantfile
sed -i '/^  #/d' ${VIRTUAL_ENV}/vm/Vagrantfile
sed -i '/^\s*$/d' ${VIRTUAL_ENV}/vm/Vagrantfile
sed -i 's/^end/  config.vm.network :private_network, ip: "192.168.99.99"\n  config.vm.network :forwarded_port, guest: 80, host: 8080\nend/g' ${VIRTUAL_ENV}/vm/Vagrantfile

```

When you run ```mkvirtualenv <project name>```, it will clone this
repository and do a little bit extra work.
