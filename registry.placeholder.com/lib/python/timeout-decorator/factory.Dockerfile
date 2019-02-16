FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 timeout-decorator==0.4.1
