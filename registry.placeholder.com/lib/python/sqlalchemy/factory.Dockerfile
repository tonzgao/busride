FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 sqlalchemy==1.2.18
