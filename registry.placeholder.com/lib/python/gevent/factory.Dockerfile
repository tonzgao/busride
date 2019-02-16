FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 gevent==1.4.0