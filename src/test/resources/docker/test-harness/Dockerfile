FROM fedora:25

MAINTAINER Rick Broker <rbroker@xebialabs.com>

RUN dnf -y install procps net-tools pcre pcre-static python && \
    dnf clean all 
RUN pip install --upgrade pip
RUN pip install flask
RUN mkdir /cherwell

ENV FLASK_APP=/cherwell/app.py
ENV FLASK_ENV=development

COPY cherwell /cherwell

VOLUME /cherwell

EXPOSE 5000

CMD flask run --host=0.0.0.0

