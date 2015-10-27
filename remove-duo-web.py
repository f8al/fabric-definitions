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


@task()
@parallel
def remove_duo_web():
	"Removes duo splunk integration"
	if exists('/opt/splunk/lib/python2.7/site-packages/splunk/appserver/mrsparkle/controllers/.old_account.py',use_sudo=True,verbose=False):
		with cd('/opt/splunk//lib/python2.7/site-packages/splunk/appserver/mrsparkle/controllers/'):
			sudo('logger "Removing duo account.py"')
			sudo('rm -rfv account.py')
			sudo('mv .old_account.py account.py')
			sudo('logger "removing duo cache"')
			sudo('rm -rfv account.pyo')
	if exists('/opt/splunk/share/splunk/search_mrsparkle/templates/account/duoauth.html',use_sudo=True,verbose=False):
		with cd('/opt/splunk/share/splunk/search_mrsparkle/templates/account'):
			sudo('rm duoauth.html')
	if exists('/opt/splunk/share/splunk/search_mrsparkle/exposed/js/contrib/duo.web.bundled.min.js',use_sudo=True,verbose=False):
		with cd('/opt/splunk/share/splunk/search_mrsparkle/exposed/js/contrib/'):
			sudo('rm -rfv duo.web.bundled.min.js')
	if exists('/opt/splunk/lib/python2.7/site-packages/duo_web.py',use_sudo=True,verbose=False):
		with cd('/opt/splunk//lib/python2.7/site-packages/'):
			sudo('rm -rfv duo_web.py')
			sudo('rm -rfv duo_web.pyo')
	if exists('/opt/splunk/lib/python2.7/site-packages/duo_client',use_sudo=True,verbose=False):
		with cd('/opt/splunk/lib/python2.7/site-packages/'):
			sudo('rm -rfv duo_client')
	if exists('/opt/splunk',use_sudo=True,verbose=False):
		sudo('/opt/splunk/bin/splunk restart splunkweb',user='splunk')
