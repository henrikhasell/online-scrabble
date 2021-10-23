FROM python:3.9 as base

WORKDIR /application

COPY dictionary.txt requirements.txt ./
RUN pip install -r requirements.txt

COPY src/online_scrabble ./online_scrabble

FROM base as test

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY src/unit_tests ./unit_tests

RUN PYTHONPATH=${PWD} pytest --cov online_scrabble unit_tests

FROM base

ENTRYPOINT ["bash"]