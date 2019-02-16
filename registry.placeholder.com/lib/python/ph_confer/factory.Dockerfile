FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 ph_confer==1.2.7
