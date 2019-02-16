FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 psycopg2==2.7.7
