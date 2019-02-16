FROM sanic/apt_knuckles

RUN mkdir -p /tmp/build/
WORKDIR /tmp/build/

RUN echo 'deb http://nginx.org/packages/mainline/ubuntu/ xenial nginx' >> /etc/apt/sources.list && \
    echo 'deb-src http://nginx.org/packages/mainline/ubuntu/ xenial nginx' >> /etc/apt/sources.list && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys ABF5BD827BD9BF62 && \
    /scripts/download_and_dependencies.sh nginx

RUN rm -rf /tmp/build
