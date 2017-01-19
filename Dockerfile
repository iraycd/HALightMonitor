FROM jsurf/rpi-raspbian

RUN sudo apt-get -y update
RUN sudo apt-get -y install python
RUN sudo apt-get -y install python-pip

RUN mkdir /HueLightMonitor
RUN mkdir /shared
WORKDIR /HueLightMonitor
ADD ./src/main.py .
ADD ./src/wonderwareOnline.py .
ADD ./src/qhue_username.txt .

RUN pip install requests
RUN pip install qhue

CMD ["python","main.py"]