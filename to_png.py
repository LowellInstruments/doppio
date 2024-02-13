import os
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import datetime
import pytz
from utils import get_nc_files, DL_FILENAME, LON, LAT


def plot_forecast(deg, str_tz):

    # str_tz:  'America/New_York' / 'UTC'
    assert deg in ('C', 'F')
    print('\nPNG file creation START')

    for f in get_nc_files():
        # load data from .nc file downloaded before
        nc = netCDF4.Dataset(f)
        times = ma.getdata(nc.variables['time'][:])
        lat = nc.variables['lat_rho'][:]
        lon = nc.variables['lon_rho'][:]
        dt_17 = datetime.datetime(2017, 11, 1, 00, 00, 00, 0)
        y = ma.getdata(lat)
        x = ma.getdata(lon)

        for i, t in enumerate(times):
            # pivot time t ~ 55000 hours from Nov. 2017 reaches 2024
            dt_utc = (dt_17 + datetime.timedelta(hours=t)).replace(tzinfo=pytz.UTC)
            dt_tz = dt_utc.astimezone(pytz.timezone(str_tz))
            dt_s = dt_tz.strftime('%Y-%m-%d %H:%M')

            # Name the image output, lose the '.nc' extension
            filename = f'{DL_FILENAME[:-3]}_{deg}_{dt_s}.png'

            # set intensity z and plot
            lvl = np.arange(0, 30, 1)
            lvl = lvl if deg == 'C' else lvl * 1.8 + 32
            fig1, ax1 = plt.subplots()
            ax1.set_aspect('equal')
            ax1.patch.set_facecolor('0.75')
            z = ma.getdata(nc.variables['temp'][i])
            z = z if deg == 'C' else z * 1.8 + 32
            tcf = ax1.contourf(x, y, z[0], cmap='jet', levels=lvl)
            cbar = fig1.colorbar(tcf)
            cbar.set_label(f'Bottom Temp ({deg})', rotation=-90)
            # set region to plot
            plt.xlim(LON[0], LON[1])
            plt.ylim(LAT[0], LAT[1])
            plt.suptitle(f'{dt_s} {str_tz}')

            # create output PNG image
            plt.savefig(filename)
            plt.close()
            bn = os.path.basename(filename)
            print(f'built image {bn}')
