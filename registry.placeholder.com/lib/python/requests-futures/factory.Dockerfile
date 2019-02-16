FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 requests-futures==0.9.9
