FROM sanic/apt_knuckles

RUN /scripts/download_deb.sh https://code.parsehub.com/p/phfiles/raw/master/filebeat_1.3.1_amd64.deb
