#!/bin/python
from fabric.api import *
from fabric.contrib.files import exists

env.shell = "/bin/bash -c"
env.user="ssh_user"
env.password = "changeme"
env.sudo_password="changeme"
env.dedupe_hosts = "True"
env.port= "22"
env.sudo_user = "root"
env.colorize_errors = "True"
env.ignore_hostkey="True"

@task(alias='configure-minion')
@parallel
def configure_salt_minion_master():
	"modifies config to point to salt master"
	sudo('yum install epel-release -y')
	sudo('yum install salt-minion -y')
	sed('/etc/salt/minion','#master: salt','master: <MASTER IP HERE>',limit='',use_sudo=True,backup='bak' )
	sudo('chkconfig salt-minion on')
	sudo('service salt-minion start')
