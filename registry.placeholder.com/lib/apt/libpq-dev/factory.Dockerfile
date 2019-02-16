FROM sanic/apt_knuckles

RUN /scripts/download_and_dependencies.sh libpq-dev
