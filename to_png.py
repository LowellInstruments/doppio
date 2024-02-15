from datetime import datetime, timedelta
from os.path import basename
import netCDF4
import pytz
from matplotlib import pyplot as plt
from numpy import ma, arange

from dl import FM4
from utils import glob_nc_files


# area to show in map
LAT = [38, 45]
LON = [-75, -66]


def forecast_png_by_hour(deg, str_tz):
    # str_tz:  'America/New_York' / 'UTC'
    assert deg in ('C', 'F')
    print('\nbuilding PNG files')

    for f_nc in glob_nc_files():
        # load data from .nc file downloaded before
        nc = netCDF4.Dataset(f_nc)
        times = ma.getdata(nc.variables['time'][:])
        lat = nc.variables['lat_rho'][:]
        lon = nc.variables['lon_rho'][:]
        dt_17 = datetime(2017, 11, 1, 00, 00, 00, 0)
        y = ma.getdata(lat)
        x = ma.getdata(lon)

        for i, t in enumerate(times):
            # pivot time t ~ 55000 hours from Nov. 2017 reaches 2024
            delta = timedelta(hours=t)
            dt_utc = (dt_17 + delta).replace(tzinfo=pytz.UTC)
            dt_tz = dt_utc.astimezone(pytz.timezone(str_tz))
            dt_s = dt_tz.strftime(FM4)

            # name PNG image output, lose '.nc' extension
            f_png = f'{f_nc[:-3]}_{dt_s}_{deg}.png'

            # set intensity z
            lvl = arange(0, 30, 1)
            lvl = lvl if deg == 'C' else lvl * 1.8 + 32
            fig1, ax1 = plt.subplots()
            ax1.set_aspect('equal')
            ax1.patch.set_facecolor('0.75')
            z = ma.getdata(nc.variables['temp'][i])
            z = z if deg == 'C' else z * 1.8 + 32
            tcf = ax1.contourf(x, y, z[0], cmap='jet', levels=lvl)
            cbar = fig1.colorbar(tcf)
            cbar.set_label(f'Bottom Temp ({deg})',
                           rotation=-90, labelpad=25)

            # set region to plot
            plt.xlim(LON[0], LON[1])
            plt.ylim(LAT[0], LAT[1])
            plt.suptitle(f'{dt_s} {str_tz}')

            # create output PNG image
            plt.savefig(f_png, dpi=300)
            plt.close()
            bn = basename(f_png)
            print(f'{bn}')
