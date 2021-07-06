from fastapi import FastAPI
from typing import Optional
import pandas as pd
import numpy as np
from utils import grab_info_by_state

# https://towardsdatascience.com/create-your-first-rest-api-in-fastapi-e728ae649a60

# TODO: ultima atualizacion de los datos!!


def _fetch_data():
    print("Reading vaccine information")
    url = "https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip"
    df = pd.read_csv(url)

    print("Finished reading")
    return df


app = FastAPI()

vaccine_df = _fetch_data()


@app.get("/")
def home():
    return {"Hello": "FastAPI"}


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
    total_poblacion = 45808747 #TODO: no levantar de dataframe
    prim_dosis = sum(vaccine_df["primera_dosis_cantidad"])
    sec_dosis = sum(vaccine_df["segunda_dosis_cantidad"])
    aux =  {
       'primera dosis':  prim_dosis,
       'segunda dosis':  sec_dosis,
       'total_sin_vacunar': total_poblacion - prim_dosis - sec_dosis,
    }
    return aux


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
    df = df.assign(acum=pd.Series(np.ones(len(df))))
    res = df.groupby(
            by=["fecha aplicacion", "vacuna", "orden_dosis"]
        ).sum()\
        .reset_index()\
        .rename(columns={'acum':'total'})


    response = dict()
    response["header"] = list(res.columns.to_numpy())
    data = []
    for index in range(0, len(res)):
        tmp_arr = list(res.iloc[index].to_numpy())
        tmp_arr[2] = int(tmp_arr[2])
        tmp_arr[3] = int(tmp_arr[3])
        data.append(tmp_arr)

    response["content"] = data
    return response


@app.get("/greet/{name}")
def say_hi(name: str):
    return {"greeting": f"Hello, {name}"}
