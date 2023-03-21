FROM ubuntu:22.04
RUN apt-get -y update
RUN apt -y install vim
RUN apt install -y python3
RUN apt-get install -y python3-pip
RUN pip install --upgrade numpy
USER vishal