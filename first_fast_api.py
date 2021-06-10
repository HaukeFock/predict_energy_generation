from fastapi import FastAPI

# run in your machine to test: from uvicorn first_fast_api.py 

app = FastAPI()

@app.get("/")
def index:
    return "The root default output"

@app.get("/predict")
def predict(start_time, end_time):
    # call the model + predict
    
    return # dictionary of hourly prediction for timeframe



