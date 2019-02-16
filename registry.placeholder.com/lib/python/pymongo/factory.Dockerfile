FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 pymongo==3.6.0