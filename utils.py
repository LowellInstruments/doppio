from glob import glob

DL_FOL = '/tmp/doppio'


def glob_nc_files():
    return sorted(glob(f"{DL_FOL}/*.nc"))


def glob_png_files():
    return sorted(glob(f"{DL_FOL}/*.png"))


def glob_gif_files(deg):
    return sorted(glob(f"{DL_FOL}/_{deg}*.gif"))


def build_url(ds, de):
    print(f'date start -> {ds}')
    print(f'date end   -> {de}')
    u = 'https://tds.marine.rutgers.edu/thredds/ncss/roms/doppio/2017_da/his/History_Best?'
    u += 'var=temp&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start='
    u += ds + 'T%3A00%3A00%3A00Z&time_end=' + de
    u += 'T%3A00%3A00%3A00Z&timeStride=1&vertCoord=-0.9875&accept=netcdf'
    return u
