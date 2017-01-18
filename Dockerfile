FROM jsurf/rpi-raspbian

RUN apt-get update -y
RUN apt-get install python -y
RUN apt-get install python-pip -y

RUN mkdir /HueLightMonitor
RUN mkdir /shared
WORKDIR /HueLightMonitor
ADD ./src/main.py .
ADD ./src/wonderwareOnline.py .
ADD ./src/qhue_username.txt .

RUN pip install requests
RUN pip install qhue

CMD ["python","main.py"]