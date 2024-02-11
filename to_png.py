import os

import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import datetime
import pytz
from utils import get_nc_files, DL_FILENAME
from zoneinfo import ZoneInfo


def plot_forecast(deg, str_tz):
    assert deg in ('C', 'F')
    # str_tz:  'America/New_York' / 'UTC'

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
            start = datetime.datetime(2017, 11, 1, 00, 00, 00, 0)
            # start: datetime 2017-11-01 00:00:00
            # t can be around 55000 hours
            utc_stamp = (start + datetime.timedelta(hours=t)).replace(tzinfo=pytz.UTC)
            print('utc_stamp', utc_stamp)
            # utc_stamp 2024-02-14 12:00:00+00:00
            daystr2 = utc_stamp.astimezone(pytz.timezone(str_tz))
            # daystr2 datetime.datetime(2024, 2, 10, 20, 0, tzinfo=<DstTzInfo 'America/New_York' EST-1 day, 19:00:00 STD>)
            daystri2 = daystr2.strftime('%Y-%m-%d %H:%M')
            # daystri2 '2024-02-10 20:00'

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
