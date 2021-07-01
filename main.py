from fastapi import FastAPI
from typing import Optional
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# https://towardsdatascience.com/create-your-first-rest-api-in-fastapi-e728ae649a60

def _fetch_data():
    print("Reading vaccine information")
    url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19VacunasAgrupadas.csv.zip'
    df = pd.read_csv(url)

    df_vac = pd.read_csv("dash/vacunas.csv")

    print(df_vac)
    print(df_vac.columns)

    print("Finished reading")
    return df, df_vac


app = FastAPI()

vaccine_df, df_vac = _fetch_data()
@app.get("/")
def home():
    return {"Hello": "FastAPI"}

@app.get("/vaccines/by_jurisdiction/{dose_num}")
def get_vaccines_by_jurisdiction(dose_num: int):
    """
    Get the vaccine information by jurisdiction of the `{dose_num}` dose
    """
    if dose_num not in [1,2]:
        return {"Error": f"{dose_num} is not a valid dose number"}

    dose_col_to_drop = "primera_dosis_cantidad" if dose_num == 2 else "segunda_dosis_cantidad"
    result_df = df_vac.drop(['jurisdiccion_nombre', dose_col_to_drop], axis=1)
    return result_df.to_json(orient="values")

@app.get("/greet/{name}")
def say_hi(name: str):
    return {"greeting": f"Hello, {name}"}

@app.get("/find/{name}")
def find_person(name: str, important: Optional[bool] = False):
    """
    Find by name
    """
    if important: # i.e http://localhost:8000/find/roca?important=True
        return {"answer", f"I'll find {name} even if I don't know them"}

    if name == "hermione":
        answer = f"I know {name}! Best Harry Potter character"
    else:
        answer = f"I'm sorry, I haven't met {name} yet"

    return {"answer": answer}

