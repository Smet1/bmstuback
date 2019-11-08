FROM ubuntu:latest

RUN apt-get -y update &&\
    apt-get -y upgrade &&\
    apt-get -y install python3-pip

RUN apt-get install mysql-server -y &&\
    apt-get install libmysqlclient-dev -y &&\
    apt-get install libmariadbclient-dev -y

ADD requirements.txt /app/

WORKDIR /app

RUN pip3 install -r requirements.txt

ADD . /app

EXPOSE 80

RUN pwd
RUN chmod +x run.sh

CMD /app/run.sh