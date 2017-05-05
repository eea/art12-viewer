# Docker orchestration for Art 12 Consultation Tool

Clone the repository

    $ git clone https://github.com/eea/art12-viewer

During the first time deployement, create and edit the following file:

    $ cd art12-viewer/deploy/

    # setup SSH key for rsync service
    $ cp rsync.key.example rsync.key
    $ vim rsync.key

[Base docker image](https://hub.docker.com/r/eeacms/art12-viewer/)

## 1. Production

The production deployment will be done through Rancher. Depending on the
Rancher environment's version, one of the following will be used:

1. [Rancher Compose](https://docs.rancher.com/rancher/v1.4/en/cattle/rancher-compose/)

2. [Rancher CLI](https://docs.rancher.com/rancher/v1.2/en/cli/)

During the first time deployement, create and edit the following files:

    $ cd art12-viewer/deploy

    # edit environment variables values
    $ cp art12.env.example art12.env
    $ vim art12.env

### 1.1. Start stack

    $ cd art12-viewer/deploy/art12/
    $ docker-compose up -d

### 1.2. Configure _apache_ service

Copy conf file and restart container

    $ scp -P 2222 ../conf/apache.conf root@localhost:/usr/local/apache2/conf/extra/vh-my-app.conf
    $ docker-compose restart apache

### 1.3. Configure _art12-static_ service

Copy conf file and restart container

    $ scp -P 2222 ../conf/static.conf root@localhost:/etc/nginx/conf.d/default.conf
    $ docker-compose restart art12-static

### 1.4. Debugging

Please refer to points 2.5. - 2.7. below.

## 2. Development

1. Install [Docker](https://www.docker.com/).

2. Install [Docker Compose](https://docs.docker.com/compose/).

During the first time deployement, create and edit the following files:

    $ cd art12-viewer/deploy

    # edit environment variables values
    $ cp art12.env.example art12.devel.env
    $ vim art12.devel.env

A minimal configuration file could be:

    #mysql env
    MYSQL_ROOT_PASSWORD=art12

    #art12 env
    DEBUG=True
    SECRET_KEY=secret

    DB_SCHEMA=mysql
    DB_USER=art12
    DB_PASS=art12
    DB_HOST=mysql
    DB_NAME=art12


### 2.1. Local build

To use a local build, run the following command:

    $ cd art12-viewer/
    $ docker build -t art12:devel .

and in docker-compose.yml use for _art12-app_ service:

    image: art12:devel

### 2.2. Start stack

    $ cd art12-viewer/deploy/art12-devel/
    $ docker-compose up -d

### 2.3. Configure _apache_ service

Copy conf file and restart container

    $ scp -P 2222 ../conf/apache.devel.conf root@localhost:/usr/local/apache2/conf/extra/vh-my-app.conf
    $ docker-compose restart apache

### 2.4. Configure _art12-static_ service

Copy conf file and restart container

    $ scp -P 2222 ../conf/static.conf root@localhost:/etc/nginx/conf.d/default.conf
    $ docker-compose restart art12-static

### 2.5. View, check status and logs

To use the application, open a browser/tab and got to http://localhost/.

Other command line useful commands:

    $ # list services and their status
    $ docker-compose ps

    $ # view log
    $ docker-compose logs -f

If, for some reason, you want to completely delete the stack and its volumes:

    $ docker-compose stop
    $ docker-compose rm
    $ docker volume rm art12_apache art12_mysqldata art12_nginx art12_staticdata

### 2.6. _art12-app_ service

There is a mapping between your local art12 folder and the folder inside the service.
Any code change will be automatically detected and the app restarted.

    # view logs
    $ docker-compose logs -f art12-app

Still, if a syntax error occurs the service will stop working and therefore must be
manually restarted:

    # restart service
    $ docker-compose restart art12-app

Another approach is to step in the container and manually start/stop the app.
To do that, in docker-compose.yml file change for _art12-app_ service the _command_ as below:

    command: /usr/bin/tail -f /dev/null

and after:

    # upgrade service
    $ docker-compose up -d art12-app

    # step into the art12-app container
    $ docker exec -it art12devel_art12-app_1 bash

and from inside the container:

    # manually start the app
    $ python manage.py runserver -t 0.0.0.0 -p 5000

_Note: make sure you have set **DEBUG=True** in the art12.devel.env file._

### 2.7. _mysql_ service

If you need to take a closer look at the MySQL database, you can do that like below:

    # step into the mysql container
    $ docker exec -it art12devel_mysql_1 bash

    # start mysql client
    $ mysql -u root -p

    # runn SQL commands
    mysql> use DB_NAME;
    mysql> show tables;

## Copyright and license

The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The Original Code is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

## Funding

[European Environment Agency (EU)](http://eea.europa.eu)
