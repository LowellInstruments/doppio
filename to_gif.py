from os.path import basename

from PIL import Image
from utils import glob_png_files


def forecast_gif(deg):
	assert deg in ('C', 'F')

	# im: PNG images / ff: frames
	print('\nbuilding GIF files')
	im = glob_png_files()
	ff = [Image.open(i) for i in im]

	# im[-1]: 20240214_C_202402131900.png
	f_gif = f'{im[-1][:-4]}_forecast.gif'
	ff[0].save(
		f_gif,
		format='GIF',
		append_images=ff[1:],
		save_all=True,
		# how fast images rotate
		duration=len(im) * 10,
		loop=0
	)

	bn = basename(f_gif)
	print(f'{bn}\n')
