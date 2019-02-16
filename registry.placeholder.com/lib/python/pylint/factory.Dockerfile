FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 pylint==2.2.2
