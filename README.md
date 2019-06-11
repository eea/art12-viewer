Project Name
------------
The Project Name is `Art 12 Consultation Tool`

[![Travis](https://travis-ci.org/eea/art12-viewer.svg?branch=master)](https://travis-ci.org/eea/art12-viewer)
[![Docker](https://dockerbuildbadges.quelltext.eu/status.svg?organization=eeacms&repository=copernicus-insitu-db)](https://hub.docker.com/r/eeacms/art12-viewer/builds/)

Prerequisites - System packages
-------------------------------
 
These packages should be installed as superuser (root).

### Debian based systems ###

Install these before setting up an environment:

    apt-get install python-setuptools python-dev libmysqlclient-dev \
    libldap2-dev libsasl2-dev python-virtualenv mysql-server git

### RHEL based systems ###
Install Python2.7 with PUIAS: https://gist.github.com/nico4/9616638

Run these commands:

    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python2.7 -

    pip2.7 install virtualenv

    yum install mysql-server mysql git openldap-devel cyrus-sasl-devel \
    mysql-devel


Install dependencies
--------------------

We should use Virtualenv for isolated environments. The following commands will
be run as an unprivileged user in the product directory:

1.Clone the repository:


    git clone git@github.com:eea/art12-viewer.git -o origin art12
    cd art12

2.1.Create & activate a virtual environment:


    virtualenv --no-site-packages sandbox
    echo '*' > sandbox/.gitignore
    source sandbox/bin/activate

2.2.Make sure setuptools >= 0.8 is installed:

    pip install -U setuptools

3.Install dependencies:

    pip install -r requirements-dep.txt

4.Create a configuration file:

    cd art12
    mkdir -p instance
    cp settings.py.example instance/settings.py

    # Follow instructions in settings.py.example to adapt it to your needs.
    # MAPS_PATH and MAPS_URI should be filled in according to your local deployment
    # e.g: MAPS_PATH = '/Users/foo/art12/art12/static/maps/' MAPS_URI = '/static/maps/'

5.Set up the MySQL database:

    # Replace [user] and [password] with your MySQL credentials and [db_name] with the name of the database:
    mysql -u[user] -p[password] -e 'create database [db_name] CHARACTER SET utf8 COLLATE utf8_general_ci;'
    ./manage.py db upgrade


Build production
----------------

Setup the production environment like this (using an unprivileged user)::

    # install dependencies, see above
    cd /var/local/art12
    source sandbox/bin/activate

At this stage, the application is up and running. You should also configure:

    * firewall policy
    * public webserver (see vhost.conf.example for an example)
    * start supervisord with the system (see init-svisor.example as an example
      init script)


Build staging
-------------

To setup a staging environment, follow the same steps as above. Create and use
a different database (for example ``art12staging``).


Factsheet generator
-------------------

Printouts work using `wkhtmltopdf 0.12.2.1`. Using an older version may cause
problems in rendering pdfs.

If you don't have this version installed, add it to your virtualenv.

1. Go to http://wkhtmltopdf.org/downloads.html and select the build
   corresponding with your system. Copy the direct link into your clipboard.

2. Install it locally in your virtualenv

    * For RedHat-based systems in production:

            wget $PASTE_URL_COPIED_AT_STEP_1
            # $PACKAGE is the file downloaded with wget
            sudo rpm -i --prefix=/var/local/wkhtmltox-0.12.1 $PACKAGE.rpm
            # If the command fails because the file is already installed
            # copy `wkhtmltopdf` from the installation directory and skip
            # the next command
            cp /var/local/wkhtmltox-0.12.1/bin/wkhmtltopdf sandbox/bin/

    * For RedHat-based development systems:

            # If you don't work on projects that require other versions
            # Install this version globally
            wget $PASTE_URL_COPIED_AT_STEP_1
            sudo rpm -i $PACKAGE.rpm

    * For Debian based systems:

            wget $PASTE_URL_COPIED_AT_STEP_1
            dpkg-deb -x wkhtmltox-0.12.1_<your_distro>.deb sandbox
            cp sandbox/usr/local/bin/wkhtmltopdf sandbox/bin


Contacts
========


The project owner is Alex Eftimie (alex.eftimie at eaudeweb.ro)

Other people involved in this project are:

* Mihai Zamfir (mihai.zamfir at eaudeweb.ro)


Resources
=========

Hardware
--------

Minimum requirements:

 * 2048MB RAM
 * 2 CPU 1.8GHz or faster
 * 4GB hard disk space

Recommended:

 * 4096MB RAM
 * 4 CPU 2.4GHz or faster
 * 8GB hard disk space


Software
--------

Any recent Linux version.
apache2, local MySQL server


Copyright and license
=====================
