FROM sanic/apt_knuckles

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash
RUN /scripts/download_and_dependencies.sh nodejs

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
RUN /scripts/download_and_dependencies.sh yarn