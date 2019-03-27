FROM  python:3.7

EXPOSE 5000

WORKDIR /opt

RUN apt-get update && \
    apt-get install -y libldap2-dev && \
    apt-get install -y libsasl2-dev && \
    apt-get install -y libxmlsec1-dev && \
    apt-get install -y pkg-config

ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt