FROM python:3.8-slim-buster

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt --upgrade

RUN mkdir /app
RUN mkdir /app/swagger
COPY main.py /app
COPY swagger/swagger.yaml /app/swagger

EXPOSE 8180

ENTRYPOINT [ "/app/main.py" ]