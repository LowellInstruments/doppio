import datetime
import glob
import pathlib

FM2 = '%Y-%m-%d'
FM3 = '%Y%m%d'

# DS/E: date start, end
DS = datetime.datetime.utcnow()
DE = DS + datetime.timedelta(days=7)
DL_FOLDER = str(pathlib.Path.home()) + '/Downloads/doppio'
sd_fm3 = DS.strftime(FM3)
DL_FILENAME = str(DL_FOLDER) + '/DOPPIO_' + sd_fm3 + '.nc'


def get_nc_files():
    return sorted(glob.glob(f"{DL_FOLDER}/*.nc"))


def get_png_files():
    return sorted(glob.glob(f"{DL_FOLDER}/*.png"))
