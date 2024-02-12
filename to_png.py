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

    for d in get_nc_files():
        # load data from .nc file downloaded before
        nc = netCDF4.Dataset(d)
        times = ma.getdata(nc.variables['time'][:])

        for i, t in enumerate(times):

            # get info from NC data
            lat = nc.variables['lat_rho'][:]
            lon = nc.variables['lon_rho'][:]
            temp = nc.variables['temp'][i]

            # Get the time and convert to a string
            dt_17 = datetime.datetime(2017, 11, 1, 00, 00, 00, 0)
            # t ~ 55000 hours
            dt_utc = (dt_17 + datetime.timedelta(hours=t)).replace(tzinfo=pytz.UTC)
            dt_tz = dt_utc.astimezone(pytz.timezone(str_tz))
            dt_s = dt_tz.strftime('%Y-%m-%d %H:%M')

            # Set the region to plot
            ax = [LON[0], LON[1], LAT[0], LAT[1]]
            y = ma.getdata(lat)
            x = ma.getdata(lon)
            z = ma.getdata(temp)
            z = z if deg == 'C' else z * 1.8 + 32

            # Name the image output, lose the '.nc' extension
            filename = f'{DL_FILENAME[:-3]}_{deg}_{dt_s}.png'

            # Define color ramp
            lvl = np.arange(0, 30, 1)
            lvl = lvl if deg == 'C' else lvl * 1.8 + 32
            fig1, ax1 = plt.subplots()
            ax1.set_aspect('equal')
            ax1.patch.set_facecolor('0.75')
            tcf = ax1.contourf(x, y, z[0], cmap='jet', levels=lvl)
            cbar = fig1.colorbar(tcf)
            cbar.set_label(f'Bottom Temp ({deg})', rotation=-90)
            plt.xlim(ax[0], ax[1])
            plt.ylim(ax[2], ax[3])
            plt.suptitle(f'{dt_s} {str_tz}')
            plt.savefig(filename)
            plt.close()

            # create output PNG image
            bn = os.path.basename(filename)
            print(f'built image {bn}')
