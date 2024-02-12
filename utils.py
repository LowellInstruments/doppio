import datetime
import glob
import pathlib

FM2 = '%Y-%m-%d'
FM3 = '%Y%m%d'

# DS/E: date start, end
DS = datetime.datetime.now(datetime.UTC)
DE = DS + datetime.timedelta(days=7)
DL_FOLDER = str(pathlib.Path.home()) + '/Downloads/doppio'
sd_fm3 = DS.strftime(FM3)
DL_FILENAME = str(DL_FOLDER) + '/DOPPIO_' + sd_fm3 + '.nc'

# area to show in map
LAT = [38, 45]
LON = [-75, -66]


def get_nc_files():
    return sorted(glob.glob(f"{DL_FOLDER}/*.nc"))


def get_png_files():
    return sorted(glob.glob(f"{DL_FOLDER}/*.png"))


def build_url(ds, de):
    print(f'date start -> {ds}')
    print(f'date end   -> {de}')
    u = 'https://tds.marine.rutgers.edu/thredds/ncss/roms/doppio/2017_da/his/History_Best?'
    u += 'var=temp&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start='
    u += ds + 'T%3A00%3A00%3A00Z&time_end=' + de
    u += 'T%3A00%3A00%3A00Z&timeStride=1&vertCoord=-0.9875&accept=netcdf'
    return u
