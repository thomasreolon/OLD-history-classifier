FROM ubuntu:latest
#LABEL author="Thomas"

COPY app /app

WORKDIR /app

RUN apt-get update -y && apt-get install -y python3-pip python3 build-essential libpq-dev


RUN pip3 install -r requirements.txt

CMD ["python", "app.py"]
