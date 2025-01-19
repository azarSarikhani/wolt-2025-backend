FROM python:3.11-slim

RUN pip install --no-cache-dir nox

COPY lib /home/lib

COPY tests /home/tests

COPY ./.flake8 /home/.flake8

COPY ./noxfile.py /home/noxfile.py

WORKDIR /home

CMD [ "nox" ]