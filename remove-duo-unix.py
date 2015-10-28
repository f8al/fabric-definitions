#!/bin/python
from fabric.api import *
from fabric.contrib.files import exists, sed


env.shell = "/bin/bash -c"
env.user="ssh_user"
env.password = "changeme"
env.sudo_password="changeme"
env.dedupe_hosts = "True"
env.port= "22"
env.sudo_user = "root"
env.colorize_errors = "True"
env.ignore_hostkey="True"


@task()
@parallel
def remove_duo_unix():
	"Removes duo unix integration"
	sed('/etc/ssh/sshd_config','ForceCommand /usr/sbin/login_duo','     ',limit='',use_sudo=True,backup='bak' )
	sudo('service sshd restart')
	if exists('/etc/duo',use_sudo=True,verbose=False):
		with cd('/etc'):
			sudo('logger "Removing duo configs"')
			sudo('rm -rfv duo/')
	if exists('/usr/sbin/login_duo',use_sudo=True,verbose=False):
		with cd('/usr/sbin'):
			sudo('logger "Removing login_duo"')
			sudo('rm -frv login_duo')
