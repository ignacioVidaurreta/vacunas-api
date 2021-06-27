from fastapi import FastAPI
from typing import Optional

# https://towardsdatascience.com/create-your-first-rest-api-in-fastapi-e728ae649a60

app = FastAPI()

@app.get("/")
def home():
    return {"Hello": "FastAPI"}

@app.get("/greet/{name}")
def say_hi(name: str):
    return {"greeting": f"Hello, {name}"}

@app.get("/find/{name}")
def find_person(name: str, important: Optional[bool] = False):
    if important: # i.e http://localhost:8000/find/roca?important=True
        return {"answer", f"I'll find {name} even if I don't know them"}

    if name == "hermione":
        answer = f"I know {name}! Best Harry Potter character"
    else:
        answer = f"I'm sorry, I haven't met {name} yet"

    return {"answer": answer}

