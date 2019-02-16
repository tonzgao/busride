FROM sanic/tails

ADD registry.placeholder.com/lib/apt/* /tmp/lib/
RUN cd /tmp/lib && ./install.sh && rm -rf /tmp/lib
ADD registry.placeholder.com/lib/python/* /tmp/lib/
RUN cd /tmp/lib && ./install.sh && rm -rf /tmp/lib