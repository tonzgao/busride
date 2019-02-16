FROM sanic/apt_knuckles

WORKDIR /tmp/build/

RUN /scripts/download_and_dependencies.sh haproxy

RUN rm -rf /tmp/build

