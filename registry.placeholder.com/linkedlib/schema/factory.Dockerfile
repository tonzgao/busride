FROM sanic/pip_knuckles

RUN apt-get update && \
    apt-get install -y libpq-dev && \
    apt-get clean && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

ADD setup.py /tmp/pipbuild/
ADD schema /tmp/pipbuild/derpadb
RUN /scripts/bundle_local_pip.sh --python3

