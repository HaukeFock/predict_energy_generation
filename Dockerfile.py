FROM python:3.8.6-buster

COPY pred_api /api
COPY predict_energy_generation /predict_energy_generation
COPY model.joblib /model.joblib
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD uvicorn pred_api:app --host 0.0.0.0 --port $PORT