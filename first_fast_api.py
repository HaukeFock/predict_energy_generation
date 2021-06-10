from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from predict_energy_generation.predict import Energy_Generation
from predict_energy_generation.test_data import get_test_data

# run in your machine to test: from uvicorn first_fast_api.py 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return "The root default output"

@app.get("/predict")
def predict(start_time, end_time):
    # call the model + predict
    start_time = f'{start_time[:10]} {start_time[10:]}'
    end_time = f'{end_time[:10]} {end_time[10:]}'

    X_test, y_test = get_test_data(start_time, end_time)

    generation = Energy_Generation()

    result = generation.predict(X_test)
    return result.shape
    # return {date: pred for pred, date in (result.flatten(), X_test.index)}
