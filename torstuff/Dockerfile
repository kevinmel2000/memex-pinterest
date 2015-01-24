FROM ubuntu:12.04
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y tor polipo

ADD . /torstuff

WORKDIR /torstuff

CMD ["bash", "start_services.bash"]