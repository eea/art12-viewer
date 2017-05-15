# Docker orchestration for Art 12 Consultation Tool

Clone the repository

    $ git clone https://github.com/eea/art12-viewer

[Base docker image](https://hub.docker.com/r/eeacms/art12-viewer/)

## 1. Production

During the first time deployment, create and edit the following file:

    $ cd art12-viewer/deploy/

    # setup SSH key for rsync service
    $ cp rsync.key.example rsync.key
    $ vim rsync.key

The production deployment will be done through Rancher. Depending on the
Rancher environment's version, one of the following will be used:

1. [Rancher Compose](https://docs.rancher.com/rancher/v1.4/en/cattle/rancher-compose/)

2. [Rancher CLI](https://docs.rancher.com/rancher/v1.2/en/cli/)

During the first time deployment, create and edit the following files:

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

### 1.4. Factsheets

Create factsheets:

    $ docker exec -it art12-app bash
    $ ./manage.py factsheet genall [period_id]

### 1.5. Debugging

Please refer to points 2.3. - 2.7. below.

## 2. Development

1. Install [Docker](https://www.docker.com/).

2. Install [Docker Compose](https://docs.docker.com/compose/).

During the first time deployment, create and edit the following files:

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
    BIND_NAME=art12rp1_eu

    AUTH_ZOPE=False
    PDF_URL_PREFIX=http://localhost:5000
    LAYOUT_ZOPE_URL=

### 2.1. Local `docker-compose.yml` file

    $ cd art12-viewer/deploy/art12-devel/
    $ cp docker-compose.yml.example docker-compose.yml

### 2.2. Local build

To use a local build, run the following command:

    $ cd art12-viewer/
    $ docker build -t art12:devel .

and in `docker-compose.yml`, for _art12-app_ service, use:

    image: art12:devel

### 2.3. Developing and debugging

In order for your container to see the latest updates made to the code, you
have to use a volume. Uncomment the following lines in `docker-compose.yml`:

    #volumes:
    #- ../../art12:/var/local/art12/art12/

To debug the application, first override the command used by the image.
Uncomment this line:

    #command: /usr/bin/tail -f /dev/null

After starting the stack (see 2.4 below), start the development server from
inside the container. The execution will stop and wait for your commands every
time it encounters a breakpoint in your code.

    $ docker exec -it art12-app bash
    $ ./manage.py runserver -h 0.0.0.0 -p 5000


### 2.4. Start stack

    $ cd art12-viewer/deploy/art12-devel/
    $ docker-compose up -d

### 2.5. View, check status and logs

To use the application, open a browser/tab and got to http://localhost:5000/.

Other command line useful commands:

    $ # list services and their status
    $ docker-compose ps

    $ # view log
    $ docker-compose logs -f

If, for some reason, you want to completely delete the stack and its volumes:

    $ docker-compose stop
    $ docker-compose rm
    $ docker volume rm art12_mysqldata

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
    $ docker exec -it art12-app bash

and from inside the container:

    # manually start the app
    $ python manage.py runserver -t 0.0.0.0 -p 5000

_Note: make sure you have set **DEBUG=True** in the art12.devel.env file._

### 2.7. _mysql_ service

If you need to take a closer look at the MySQL database, you can do that like below:

    # step into the mysql container
    $ docker exec -it art12-mysql bash

    # start mysql client
    $ mysql -u root -p

    # runn SQL commands
    mysql> use DB_NAME;
    mysql> show tables;

To import old data, first copy the sql dumps to your mysql container:

    $ docker cp art12.sql art12-mysql:/var/lib/mysql/

    # step into the mysql container
    $ docker exec -it art12-mysql bash

    # start mysql interpreter
    $ mysql -u art12 -p

    # import data
    mysql> use art12;
    mysql> source /var/lib/mysql/art12.sql

Do the same set of operations for `art12rp1_eu` database.

### 2.8. Factsheets

Create factsheets:

    $ docker exec -it art12-app bash
    $ ./manage.py factsheet genall [period_id]

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
