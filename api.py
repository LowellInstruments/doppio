#!/usr/bin/env python3

import uvicorn
from fastapi import FastAPI
import os
from fastapi.responses import FileResponse
from utils import DL_FILENAME, DS, DE


DDN_PORT_API = 5588
NAME_EXE_API = "main_doppio_api"
PID_FILE_API = "/tmp/{}.pid".format(NAME_EXE_API)


app = FastAPI()


@app.get("/get_forecast_c")
async def get_forecast_c():
    f = f'/tmp/{DL_FILENAME[:-3]}_forecast_C.gif'
    return FileResponse(path=f, filename=os.path.basename(f))


@app.get("/get_forecast_f")
async def get_forecast_f():
    f = f'/tmp/{DL_FILENAME[:-3]}_forecast_F.gif'
    return FileResponse(path=f, filename=os.path.basename(f))


def main_api():
    uvicorn.run(app, host="0.0.0.0", port=DDN_PORT_API)


if __name__ == "__main__":
    main_api()
