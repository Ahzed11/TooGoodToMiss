FROM python:3.10

WORKDIR /usr/src/app

RUN pip install tgtg
RUN pip install matrix-nio
RUN pip install slackclient

COPY main.py .

CMD [ "python", "main.py" ]
