FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 pytest==4.2.1 pytest-timeout==1.3.3