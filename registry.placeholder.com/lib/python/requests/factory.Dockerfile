FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 requests==2.21.0

