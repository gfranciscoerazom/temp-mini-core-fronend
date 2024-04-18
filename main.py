from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn  # Library for serving the API
from fastapi import FastAPI, Query, Request  # Import the FastAPI class
import requests

app = FastAPI()  # Create an instance of the FastAPI class

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(
    request: Request,
    descripcion: str = Query(None),
    fecha: str = Query(None),
    latitud: str = Query(None),
    longitud: str = Query(None),
    publicacionId: str = Query(None),
    tipo: str = Query(None)
):
    response = requests.get(
        "http://127.0.0.1:5000/publicaciones/filter").json()

    if descripcion:
        response = list(filter(lambda x: descripcion.casefold()
                        in x["descripcion"].casefold(), response))

    if fecha:
        response = list(filter(lambda x: x["fecha"] == fecha, response))

    if latitud:
        response = list(filter(lambda x: x["latitud"] == latitud, response))

    if longitud:
        response = list(filter(lambda x: x["longitud"] == longitud, response))

    if publicacionId:
        response = list(
            filter(lambda x: x["publicacionId"] == int(publicacionId), response))

    if tipo:
        response = list(filter(lambda x: tipo.casefold()
                        in x["tipo"].casefold(), response))

    return templates.TemplateResponse("index.html", {"request": request, "publicaciones": response})


# Entry point for the API
if __name__ == "__main__":
    # Run the application using uvicorn and enable auto-reload
    uvicorn.run("main:app", reload=True)
