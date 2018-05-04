FROM nvidia/cuda

LABEL maintainer="behar@veliqi.de"

ENV DEBIAN_FRONTEND noninteractive

ADD . .

RUN apt-get -yq update
RUN apt-get -yq install software-properties-common python-software-properties
RUN apt-get -yq install python3-pip
RUN apt-get -yq install vim

RUN pip3 install --upgrade -r requirements.txt

ENTRYPOINT [ "python3", "csv2mongo.py" ]
