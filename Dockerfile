FROM python:3.8.6-buster

COPY first_fast_api.py /first_fast_api.py
COPY predict_energy_generation /predict_energy_generation
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn first_fast_api:app --host 0.0.0.0 --port $PORT
