from fastapi import FastAPI
from typing import Optional
import pandas as pd
from utils import df_to_json
# https://towardsdatascience.com/create-your-first-rest-api-in-fastapi-e728ae649a60

def _fetch_data():
    print("Reading vaccine information")
    url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip'
    df = pd.read_csv(url)

    print("Finished reading")
    return df


app = FastAPI()

vaccine_df = _fetch_data()
@app.get("/")
def home():
    return {"Hello": "FastAPI"}

@app.get("/vaccines/by_state/{dose_num}")
def get_vaccines_by_state(dose_num: int):
    """
    Get the vaccine information by state of the `{dose_num}` dose
    """
    if dose_num not in [1,2]:
        return {"Error": f"{dose_num} is not a valid dose number"}

    dose_col = "primera_dosis_cantidad" if dose_num == 1 else "segunda_dosis_cantidad"
    return df_to_json(vaccine_df, dose_col)

@app.get("/greet/{name}")
def say_hi(name: str):
    return {"greeting": f"Hello, {name}"}

