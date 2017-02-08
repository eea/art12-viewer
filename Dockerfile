FROM python:2.7-slim
MAINTAINER "EEA: IDM2 C-TEAM" <eea-edw-c-team-alerts@googlegroups.com>

ENV WORK_DIR=/var/local/art12

RUN runDeps="curl vim build-essential netcat mysql-client libmysqlclient-dev python-dev libldap2-dev libsasl2-dev libssl-dev" \
 && apt-get update \
 && apt-get install -y --no-install-recommends $runDeps \
 && rm -vrf /var/lib/apt/lists/*

COPY . $WORK_DIR/
WORKDIR $WORK_DIR

RUN pip install -U setuptools \
 && pip install -r requirements-dep.txt --trusted-host eggshop.eaudeweb.ro \
 && mv docker-entrypoint.sh /bin/

ENTRYPOINT ["docker-entrypoint.sh"]
