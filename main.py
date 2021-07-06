from fastapi import FastAPI
from typing import Optional
import pandas as pd
import numpy as np
from utils import grab_info_by_state
import json

# https://towardsdatascience.com/create-your-first-rest-api-in-fastapi-e728ae649a60

# TODO: ultima atualizacion de los datos!!


def _fetch_data():
    print("Reading vaccine information")
    url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip"
    df = pd.read_csv(url)
    print("Finished reading")
    return df


def fetch_recepcion_de_vacunas():
    print("Reading reception data")
    url = "http://datos.salud.gob.ar/dataset/7e69d4b4-535d-4d4d-ad4a-362b6a1f4468/resource/d2851fa6-b105-4f15-b352-dd3d792bd526/download/2021-06-29-actas-de-recepcion-vacunas.xlsx"
    df = pd.read_excel(url)
    print("FInish Reading")
    return df


app = FastAPI()

vaccine_df = _fetch_data()
vaccine_reception = fetch_recepcion_de_vacunas()


@app.get("/")
def home():
    return {"Hello": "FastAPI"}


@app.get("/vaccines/reception_qty")
def get_reception_vaccines_qty():
    """
    Get number of vaccines that arrived in the country
    """
    qty = vaccine_reception["dosis_recibidas"].sum()
    aux = {"dosis_recibidas": int(qty)}
    return aux


@app.get("/vaccines/qty")
def get_vaccines_qty():
    """
    Get administered vaccines quantity by name and total and its percentage
    """
    qty = vaccine_df.groupby("vacuna_nombre").apply(
        lambda s: pd.Series(
            {
                "Cantidad": (
                    s["primera_dosis_cantidad"] + s["segunda_dosis_cantidad"]
                ).sum()
            }
        )
    )
    qty["Porcentaje"] = (qty["Cantidad"] / qty["Cantidad"].sum()) * 100
    qty = qty.sort_values(by=["Porcentaje"], ascending=False)
    qty.loc["Total"] = qty.sum()
    return qty


@app.get("/vaccines/doses")
def get_number_vaccines_per_dose():
    """
    Get the number of doses for first and second doses of vaccines
    """
    total_poblacion = 45808747
    prim_dosis = sum(vaccine_df["primera_dosis_cantidad"])
    sec_dosis = sum(vaccine_df["segunda_dosis_cantidad"])
    aux = {
        "primera_dosis": int(prim_dosis),
        "segunda_dosis": int(sec_dosis),
        "total_sin_vacunar": int(total_poblacion - prim_dosis - sec_dosis),
    }
    return json.dumps(aux)


@app.get("/vaccines/by_state/{dose_num}")
def get_vaccines_by_state(dose_num: int):
    """
    Get the vaccine information by state of the `{dose_num}` dose
    """
    if dose_num not in [1, 2]:
        return {"Error": f"{dose_num} is not a valid dose number"}

    dose_col = "primera_dosis_cantidad" if dose_num == 1 else "segunda_dosis_cantidad"
    return grab_info_by_state(vaccine_df, dose_col)


@app.get("/vaccines/by_date")
def get_vaccines_by_date():
    """
    Get the vaccine information by date. Returns data for every vaccine and both doses.
    Response Format:
    An `array` where each element has as array with the following format:
    ```
    [date, vaccine_name, dose_num, qty]
    ```
    """
    df = pd.read_csv("dates_vaccines_qty.csv")

    response = dict()
    response["header"] = list(df.columns.to_numpy())
    data = []
    for index in range(0, len(df)):
        tmp_arr = list(df.iloc[index].to_numpy())
        tmp_arr[2] = int(tmp_arr[2])
        data.append(tmp_arr)

    response["content"] = data
    return response


@app.get("/greet/{name}")
def say_hi(name: str):
    return {"greeting": f"Hello, {name}"}
