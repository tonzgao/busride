FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 transaction==2.4.0
