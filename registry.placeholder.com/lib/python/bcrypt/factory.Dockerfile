FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 bcrypt==3.1.6
