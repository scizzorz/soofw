* title = Set Up a Remote Git Repository
* datetime = 3/16/2013 3:01pm
* tags = git

Make the remote repository:

	$ ssh user@host.com
	$ mkdir project.git
	$ cd project.git
	$ git init --bare

Connect an existing repository to the new remote repository:

	$ cd project
	$ git remote add origin user@host.com:project.git
	$ git push -u origin master

Clone a remote repository:

	$ git clone user@host.com:project.git
