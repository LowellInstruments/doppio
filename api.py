#!/usr/bin/env python3

from os.path import basename

from fastapi import FastAPI
from fastapi.responses import FileResponse
from uvicorn import run

from utils import glob_gif_files

DDN_PORT_API = 5588
NAME_EXE_API = "main_doppio_api"
PID_FILE_API = "/tmp/{}.pid".format(NAME_EXE_API)


app = FastAPI()


@app.get("/get_forecast_c")
async def get_forecast_c():
    f = glob_gif_files('C')[-1]
    return FileResponse(path=f, filename=basename(f))


@app.get("/get_forecast_f")
async def get_forecast_f():
    f = glob_gif_files('F')[-1]
    return FileResponse(path=f, filename=basename(f))


def main_api():
    run(app, host="0.0.0.0", port=DDN_PORT_API)


if __name__ == "__main__":
    main_api()
