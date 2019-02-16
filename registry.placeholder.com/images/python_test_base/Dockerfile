FROM registry.placeholder.com/images/db_tails

ADD registry.placeholder.com/lib/python/* /tmp/lib/
RUN cd /tmp/lib && ./install.sh && rm -rf /tmp/lib

ADD test.sh /
RUN chmod 755 /test.sh
