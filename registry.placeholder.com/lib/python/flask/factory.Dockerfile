FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 Flask==1.0.2
