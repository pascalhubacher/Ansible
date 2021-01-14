###############################################################################
# use an existing docker image 
FROM ubuntu

WORKDIR /opt
RUN apt update -y && apt upgrade -y && apt install build-essential libssl-dev libffi-dev python-dev -y && apt install python3-pip -y && apt install python3-venv -y && apt install git -y
RUN git clone https://github.com/ansible/ansible.git

WORKDIR /opt/ansible

#copy packages that are needed to 
COPY ./requirements.txt .

RUN python3 -m venv venv

RUN . venv/bin/activate && pip3 install -r requirements.txt && pip3 install HitachiBlockAPI
ENTRYPOINT /bin/bash

#docker build -t pascalhubacher/ansible:latest .
#docker run -it pascalhubacher/ansible bash