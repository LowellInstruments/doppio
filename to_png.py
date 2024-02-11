import os

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import datetime
import pytz
from utils import get_nc_files, DL_FILENAME


def plot_forecast(deg, str_tz):
    assert deg in ('C', 'F')
    # str_tz:  'America/New_York' / 'UTC'

    print('\nPNG file creation START')

    for d in get_nc_files():
        # load data from .nc file downloaded before
        nc = netCDF4.Dataset(d)
        times = ma.getdata(nc.variables['time'][:])

        for i, t in enumerate(times):
            # Get the lat/lon coordinates
            lat = nc.variables['lat_rho'][:]
            lon = nc.variables['lon_rho'][:]

            # Get the temperature values
            temp = nc.variables['temp'][i]

            # Get the time and convert to a string
            start = datetime.datetime(2017, 11, 1, 00, 00, 00, 0)
            dtime = start + datetime.timedelta(hours=t)
            daystri = dtime.strftime('%Y-%m-%d %H:%M')
            daystr = datetime.datetime.strptime(daystri, '%Y-%m-%d %H:%M')
            utc_stamp = daystr.replace(tzinfo=pytz.UTC)
            daystr2 = utc_stamp.astimezone(pytz.timezone(str_tz))
            daystri2 = daystr2.strftime('%Y-%m-%d %H:%M')

            # Set the region to plot
            ax = [-75, -66, 38, 45]
            ind = np.argwhere((lon >= ax[0]) & (lon <= ax[1]) &
                              (lat >= ax[2]) & (lat <= ax[3]))
            y = ma.getdata(lat)
            x = ma.getdata(lon)
            z = ma.getdata(temp)
            if deg == 'F':
                z = z * 1.8 + 32

            # Name the image output, lose the '.nc' extension
            filename = f'{DL_FILENAME[:-3]}_{deg}_{daystri2}.png'

            # Define color ramp
            levels = np.arange(0, 30, 1)
            if deg == 'F':
                levels = levels * 1.8 + 32
            fig1, ax1 = plt.subplots()
            ax1.set_aspect('equal')
            ax1.patch.set_facecolor('0.75')
            tcf = ax1.contourf(x, y, z[0], cmap='jet', levels=levels)
            cbar = fig1.colorbar(tcf)
            cbar.set_label(f'Bottom Temp ({deg})', rotation=-90)
            plt.xlim(ax[0], ax[1])
            plt.ylim(ax[2], ax[3])
            plt.suptitle(f'{daystri2} {str_tz}')
            plt.savefig(filename)
            plt.close()

            # create output PNG image
            bn = os.path.basename(filename)
            print(f'built image {bn}')
