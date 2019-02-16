FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 alembic==1.0.7
