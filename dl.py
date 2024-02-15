from datetime import datetime, UTC, timedelta
from os.path import isdir, basename
from pathlib import Path
from shutil import rmtree
from time import time

from requests import get

from utils import build_url, DL_FOL

FM2 = '%Y-%m-%d'
FM3 = '%Y%m%d'
FM4 = '%Y%m%d%H%M'
FM5 = '%Y %b %d %Hh'


def get_download_nc_file_path(ds):
    return f'{DL_FOL}/{ds.strftime(FM4)}.nc'


def _download_url(url, fn):
    try:
        r = get(url)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return url
    except Exception as e:
        print('Exception in download_url():', e)


def forecast_data_download(ds=datetime.now(UTC),
                           de=datetime.now(UTC) + timedelta(days=7)):

    print(f'\ndownloading NC files')
    print(f'output dir -> {DL_FOL}')

    # create download destination folder
    if isdir(DL_FOL):
        rmtree(DL_FOL)
    Path(DL_FOL).mkdir(parents=True, exist_ok=True)

    # download remote NC file
    t = time()
    u = build_url(ds.strftime(FM2), de.strftime(FM2))
    f = get_download_nc_file_path(ds)
    _download_url(u, f)
    t = time() - t
    print(f'file saved -> {basename(f)}')
    print(f'download took {int(t)} seconds')


if __name__ == '__main__':
    forecast_data_download()
