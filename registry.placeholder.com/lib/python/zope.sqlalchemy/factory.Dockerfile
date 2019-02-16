FROM sanic/pip_knuckles

RUN /scripts/bundle_pip.sh --python3 zope.sqlalchemy==1.1
