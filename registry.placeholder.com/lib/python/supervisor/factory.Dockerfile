FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 supervisor==3.3.5

