from PIL import Image
from utils import get_png_files, DL_FILENAME


def create_gif(deg):
	assert deg in ('C', 'F')

	print('\nGIF file creation START')

	imgs = get_png_files()
	frames = []
	for i in imgs:
		new_frame = Image.open(i)
		frames.append(new_frame)

	# Name the GIF image output
	filename = f'{DL_FILENAME[:-3]}_forecast_{deg}.gif'

	frames[0].save(
		filename,
		format='GIF',
		append_images=frames[1:],
		save_all=True,
		duration=len(imgs)*1,
		loop=0
	)

	print(f'GIF file creation END -> {filename}\n')
