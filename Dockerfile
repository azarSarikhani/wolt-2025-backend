FROM python:3.11-slim

COPY app /home/app

COPY lib /home/lib

RUN python -m pip install -e /home/lib

EXPOSE 8080

WORKDIR /home

CMD [ "python", "app/app.py" ]
