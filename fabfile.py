from __future__ import with_statement
from fabric.api import show, local, settings, prefix, abort, run, cd, env, require, hide, execute
from fabric.contrib.console import confirm
from fabric.network import disconnect_all
from fabric.colors import green as _green, yellow as _yellow, red as _red
from fabric.contrib.files import exists
from fabric.utils import error
import os
import time

env.user = "root"

env.warn_only = False
env.password = "metc123#"
"""
This is the file which remotely makes an ec2 instance for the use of this repository
"""

def before_env():
	""""
	This method should be run before installing virtual environment as it will install python pip
	required to install virtual environment

	"""
	run("sudo apt-get update")
	run("sudo apt-get upgrade")
	run("sudo apt-get install -y python-pip")

def after_env():
	"""
	This method activates the virtual environment and in virtual environment installs the required dependicies
	and should be run after installing virtual environement
	"""
	with prefix("cd Cyclone2 &&source bin/activate && cd Authentication"):
		run("sudo apt-get install -y libevent-dev")
		run("sudo apt-get install -y python-all-dev")
		run("sudo apt-get install -y ipython")
		run("sudo apt-get install -y libxml2-dev")
		run("sudo apt-get install -y libxslt1-dev") 
		run("sudo apt-get install -y python-setuptools python-dev build-essential")
		run("sudo apt-get install -y libxml2-dev libxslt1-dev lib32z1-dev")
		run("sudo apt-get install -y python-lxml")
		run("sudo apt-get install -y python-dev")
		run("sudo apt-get install -y zlibc zlib1g zlib1g-dev")

def virtual_env():
		"""
		This method installs the virual environment and after installing virtual environment installs the git.
		After installing the git installs the reuiqred repository
		"""

		run("sudo pip install virtualenv")
		if not exists("Cyclone2"):
			run("virtualenv --no-site-packages Cyclone2")
		with cd("Cyclone2"):
			run("sudo apt-get install -y git")
			with prefix("source bin/activate"):
				if not exists("/applogs", use_sudo=True):
					run("sudo mkdir /applogs")
				if not exists("Cyclone2/Authentication", use_sudo=True):	
					run("https://github.com/kaali-python/Authentication.git")


def installing_requirements():
	"""
	This function installs all the requirements required to run the package with the help of requirements.txt
	"""
	with prefix("cd Cyclone2 &&source bin/activate && cd Authentication"):
		run("sudo pip install -r /requirements.txt")

def update_git():
	"""
	This method will be run everytime the git repository is updated on the main machine.This clones the pushed updated 
	repository on the git on the remote server
	"""
	with prefix("cd Cyclone2 &&source bin/activate && cd Authentication"):
		run("git pull origin master")


def nginx():
	"""
	This function installs nginx on the remote server and replaces its conf file with the one available in the
	git repository.Finally restart the nginx server
	"""
	with prefix("cd Cyclone2"):
		run("sudo apt-get install -y nginx")
	#with prefix("cd /home/ubuntu/VirtualEnvironment/news_classification/configs"):
	#	run("sudo cp nginx.conf /etc/nginx/nginx.conf")



def nginx_status():
	    """
	    Check if nginx is installed.
	    """
	    with settings(hide("running", "stderr", "stdout")):
	    	result = run('if ps aux | grep -v grep | grep -i "nginx"; then echo 1; else echo ""; fi')
	    	if result:
			    print (_green("Nginx is running fine......................"))
	    	else:
			    print (_red("Nginx is not running ......................"))
			    confirmation = confirm("Do you want to trouble shoot here??", default=True)
			    if confirmation:
				    print (_green("Checking nginx configuration file"))
				    with show("debug", "stdout", "stderr"):
				    	run("sudo nginx -t")
				    	run("sudo service nginx restart")
				    	run("sudo tail -n 50 /applogs/nginx_error.logs")
		return 


def mongo():
	"""
	This method installs the mongodb database on the remote server.It after installing the mongodb replaces the 
	mongodb configuration with the one available in the git repository.

	"""
	with prefix("cd Cyclone2"):
		run("sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10")
		run("echo -e 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list")
		run("sudo apt-get update")
		run("sudo apt-get install -y mongodb-10gen")
#		run("sudo cp configs/mongodb.conf /etc/mongodb.conf")
	run("sudo rm -rf  /var/lib/mongodb/mongod.lock")
	run("sudo service mongodb restart")


def mongo_status():
	    """
	    Check if nginx is installed.
	    """
	    with settings(hide("running", "stderr", "stdout")):
	    	result = run('if ps aux | grep -v grep | grep -i "mongodb"; then echo 1; else echo ""; fi')
	    	if result:
			    print (_green("Mongodb is running fine......................"))
	    	else:
			    print (_red("Mongodb is not running ......................"))
			    confirmation = confirm("Do you want to trouble shoot here??it will delete mongo.lock file", default=True)
			    if confirmation:
					run("sudo rm -rf  /var/lib/mongodb/mongod.lock ")
				    	run("sudo service mongodb restart")
		return 


def reboot():
	run("sudo reboot")


def status():
	print(_green("Connecting to EC2 Instance..."))	
	run("free -m")
	execute(mongo_status)
	execute(nginx_status)
	print(_yellow("...Disconnecting EC2 instance..."))
	disconnect_all()



def update():
	print(_green("Connecting to EC2 Instance..."))	
	execute(update_git)
	execute(update_nginx_conf)
	execute(nginx_status)
		
	print(_yellow("...Disconnecting EC2 instance..."))
	disconnect_all()




def deploy():
	print(_green("Connecting to EC2 Instance..."))	
	execute(before_env)
	execute(virtual_env)
	execute(after_env)
	execute(installing_requirements)
	execute(nginx)
	execute(mongo)
	execute(status)
	execute(install_phantomjs)
	print(_yellow("...Disconnecting EC2 instance..."))
	run("sudo reboot")
	disconnect_all()

