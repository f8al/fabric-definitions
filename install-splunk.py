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


@task(alias='install-splunk')
@serial
def install_splunk_package(splunkFile):
        if exists('/opt/splunk/bin',use_sudo=True, verbose=False):
                with cd('/opt/splunk/bin'):
                        sudo('./splunk stop')
                        sudo('tar -czvf /home/splunkadm/backup-`date +"%Y_%m_%d"`.tar.gz /splunk/etc')
                        sudo('tar -xzf /tmp/%s -C /opt' % splunkFile )
                        sudo('chown -R splunkadm:splunkadm /opt/splunk')
                        sudo('/opt/splunk/bin/splunk start --answer-yes --no-prompt --accept-license')
                        sudo('./splunk version')       
        elif exists('/opt/splunk/bin',use_sudo=True, verbose=False) == False:
                sudo('tar -xzf /tmp/%s -C /opt' % splunkFile)
                sudo('cat /opt/splunk/etc/splunk-launch.conf.default > /opt/splunk/etc/splunk-launch.conf')
                sudo('chmod 644 /opt/splunk/etc/splunk-launch.conf')
                sudo('chown -R splunkadm:splunkadm /opt/splunk')
                with cd('/opt/splunk/bin'):
                        sudo('/opt/splunk/bin/splunk start --answer-yes --no-prompt --accept-license')
                        sudo('./splunk version')
                        sudo('./splunk stop')
                sudo('chown -R splunkadm. /opt/splunk')
