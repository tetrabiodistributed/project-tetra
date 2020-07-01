FROM golang:latest
EXPOSE 8000
RUN apt update \
    && apt install -y libzmq5-dev \
                      python3-zmq \
                      supervisor \
                      python3-pip
RUN go get github.com/pebbe/zmq4 && go get github.com/gorilla/websocket

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /src/zmq_proxy/static
RUN mkdir -p /src/zmq_proxy/TestData
WORKDIR /src/zmq_proxy
COPY main.go /src/zmq_proxy
COPY static /src/zmq_proxy/static
RUN go build

COPY requirements.txt /src/zmq_proxy
RUN pip3 install -r /src/zmq_proxy/requirements.txt
COPY *.py /src/zmq_proxy/
COPY TestData/20200609T2358Z_patrickData.txt /src/zmq_proxy/TestData
COPY services.conf /etc/supervisor/conf.d/services.conf
CMD ["/usr/bin/supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf"]
