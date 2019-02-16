FROM sanic/apt_knuckles

RUN sudo add-apt-repository ppa:deadsnakes/ppa
RUN /scripts/download_and_dependencies.sh python3.5 python3-pip
