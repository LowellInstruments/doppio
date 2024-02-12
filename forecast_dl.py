import pathlib
import requests
import time
from utils import (FM2, DL_FOLDER, DS,
                   DE, DL_FILENAME, build_url)


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

    # print(f'DOWNLOADER removing old results folder {DL_FOLDER}')
    # shutil.rmtree(DL_FOLDER)

    # create new output folder
    pathlib.Path(DL_FOLDER).mkdir(parents=True, exist_ok=True)

    # ds/e: date start/end
    u = build_url(ds.strftime(FM2), de.strftime(FM2))

    # download remote NC file
    t = time.time()
    _download_url(u, fn)
    t = time.time() - t
    print(f'DOWNLOADER took {int(t)} seconds\n')


# to test this single file
if __name__ == '__main__':
    forecast_downloader(DS, DE, DL_FILENAME)
