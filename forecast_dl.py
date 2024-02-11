import pathlib
import requests
import time
from utils import FM2, DL_FOLDER, DS, DE, DL_FILENAME


def _download_url(url, fn):
    try:
        r = requests.get(url)
        with open(fn, 'wb') as f:
            f.write(r.content)
        return url
    except Exception as e:
        print('Exception in download_url():', e)


def forecast_downloader(ds, de, fn):

    print(f'\nDOWNLOADER START, output folder: \n\t{DL_FOLDER}')
    # so results folder is always new
    # print(f'DOWNLOADER removing old results folder {DL_FOLDER}')
    # shutil.rmtree(DL_FOLDER)
    pathlib.Path(DL_FOLDER).mkdir(parents=True, exist_ok=True)

    print(f'date start -> {ds}')
    print(f'date end   -> {de}')

    # ds/e: date start/end
    sd_fm2 = ds.strftime(FM2)
    ed_fm2 = de.strftime(FM2)
    u = 'https://tds.marine.rutgers.edu/thredds/ncss/roms/doppio/2017_da/his/History_Best?'
    u += 'var=temp&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start='
    u += sd_fm2 + 'T%3A00%3A00%3A00Z&time_end=' + ed_fm2
    u += 'T%3A00%3A00%3A00Z&timeStride=1&vertCoord=-0.9875&accept=netcdf'

    # download the remote NC file
    s = time.time()
    _download_url(u, fn)
    t = time.time() - s
    print(f'DOWNLOADER took {int(t)} seconds\n')


# to test this single file
if __name__ == '__main__':
    forecast_downloader(DS, DE, DL_FILENAME)
