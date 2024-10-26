from PIL import Image
import os

image_folder = '../smai_1/gif'
output_gif = 'output.gif'

files = [f for f in os.listdir(image_folder) if f.endswith(('jpg', 'jpeg', 'png'))]
files.sort() 

images = [Image.open(os.path.join(image_folder, file)) for file in files]

images = [img.convert('RGB') for img in images]

# Saving images as GIF
images[0].save(
    output_gif,
    save_all=True,
    append_images=images[1:],
    optimize=False,
    duration=250,  
    loop=0         
)

print(f'GIF saved as {output_gif}')
