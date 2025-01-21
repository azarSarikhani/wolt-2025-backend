# Price Calculator API 

This repository includes solution for Wolt's 2025 internship code challenge. The app calculates price
based on the requirements specified in wolt 2025 subject instruction.

## **Environments to Run**

- The app can be run locally as a standalone API that listens on port 8080. 
- The app can be built and run using docker. The docker app runs on port 8080 of the docker container that is maped to port 8080 of the host. 
- The app could be test run using Git hub runners. The Github action CI pipeline tests the app and runs it for 10 seconds to verify there are no errors, then gracefully kills the API process.

---

## **Requirements**

- Python 3.11 is used to develop and test this API. Python 3.11 is not required and the API can work with python 3.10 and higher, but it has not been tested with all python versions. Python 3.11 is recommanded.

---

## **Usage**

To run the API locally, go to the root of the repo. We can create a virtual environmrnt then run the app, but if you are happy with pip installing all of the packages just run:

```bash
python3 -m pip install -e lib
python3 app/app.py
```

To create a virtual environment:

```bash
mkdir venv
python3 -m venv venv/wolt-2025
source venv/wolt-2025/bin/activate
```

To run the tests locally, go to the root of the repo and run: 

```bash
pip install nox
nox
```


To run the docker container, go to the root of the repo and run:

```bash
docker compose up --build
```
