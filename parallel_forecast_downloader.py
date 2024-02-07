import os
import pathlib
import shutil

import requests
import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from utils import FM2, DL_FOLDER


def _download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    try:
        r = requests.get(url)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return url, time.time() - t0
    except Exception as e:
        print('Exception in download_url():', e)


def _download_parallel(args):
    cpus = cpu_count()
    results = ThreadPool(cpus - 1).imap_unordered(_download_url, args)
    for result in results:
        print(f'url downloaded in {int(result[1])} seconds')


def forecast_downloader(ds, de, filename):

    print('\nDOWNLOADER START')
    print(f'date start -> {ds}')
    print(f'date end   -> {de}')

    # ds/e: date start/end
    urls = list()
    sd_fm2 = ds.strftime(FM2)
    ed_fm2 = de.strftime(FM2)
    urls.append('https://tds.marine.rutgers.edu/thredds/ncss/roms/doppio/2017_da/his/History_Best?'
                'var=temp&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=' + sd_fm2 +
                'T%3A00%3A00%3A00Z&time_end=' + ed_fm2 +
                'T%3A00%3A00%3A00Z&timeStride=1&vertCoord=-0.9875&accept=netcdf')

    # so results folder is always new
    print(f'DOWNLOADER removing old results folder {DL_FOLDER}')
    shutil.rmtree(DL_FOLDER)

    # create results folder
    print(f'DOWNLOADER creating new results folder {DL_FOLDER}')
    pathlib.Path(DL_FOLDER).mkdir(parents=True, exist_ok=True)

    files = list()
    files.append(filename)
    inputs = zip(urls, files)

    # download the thing
    _download_parallel(inputs)

    print('DOWNLOADER FINISH\n')
