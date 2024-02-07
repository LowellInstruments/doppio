from doppio_plots_to_gif_forecasts import create_gif
from parallel_forecast_downloader import forecast_downloader
from plot_forecast import plot_forecast
from utils import DS, DE, DL_FILENAME


def main():

    # download the data
    forecast_downloader(DS, DE, DL_FILENAME)

    # create png files of it
    deg = 'C'
    str_tz = 'UTC'
    plot_forecast(deg, str_tz)

    # create gif of previous png files
    create_gif(deg)


if __name__ == '__main__':
    main()
