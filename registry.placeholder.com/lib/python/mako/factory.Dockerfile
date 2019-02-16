FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 mako==1.0.7
