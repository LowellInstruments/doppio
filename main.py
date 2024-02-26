#!/usr/bin/env python3

from to_gif import forecast_gif
from dl import forecast_data_download
from to_png import forecast_png_by_hour


def main():
    forecast_data_download()
    deg = 'F'
    str_tz = 'America/New_York'
    forecast_png_by_hour(deg, str_tz)
    forecast_gif(deg)


if __name__ == '__main__':
    main()
