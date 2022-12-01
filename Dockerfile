FROM python:3.7

RUN mkdir /Lost_Found_Server 
RUN mkdir /Lost_Found_Server/Lost_Found_app

WORKDIR /Lost_Found_Server/Lost_Found_app

COPY . . 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 
WORKDIR Lost_Found_app/ 