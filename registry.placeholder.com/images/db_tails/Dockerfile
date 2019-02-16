FROM registry.placeholder.com/images/bloated_tails

ADD registry.placeholder.com/lib/apt/* /tmp/lib/
RUN cd /tmp/lib && ./install.sh && rm -rf /tmp/lib
ADD registry.placeholder.com/lib/python/* /tmp/lib/
RUN cd /tmp/lib && ./install.sh && rm -rf /tmp/lib

ADD schema /busride/linkedlib/schema
RUN cd /busride/linkedlib/schema && pip3 install -e ./
