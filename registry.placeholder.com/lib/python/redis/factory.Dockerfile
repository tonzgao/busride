FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 redis==3.1.0
