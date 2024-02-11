import os

from PIL import Image
from utils import get_png_files, DL_FILENAME


def create_gif(deg):
	assert deg in ('C', 'F')

	# im: PNG images / ff: frames
	im = get_png_files()
	ff = [Image.open(i) for i in im]
	output_gif_name = f'{DL_FILENAME[:-3]}_forecast_{deg}.gif'
	ff[0].save(
		output_gif_name,
		format='GIF',
		append_images=ff[1:],
		save_all=True,
		duration=len(im),
		loop=0
	)

	bn = os.path.basename(output_gif_name)
	print(f'built GIF -> {bn}\n')
