import os
import Augmentor
from PIL import Image
import shutil

# Path to images and labels
image_dir = "./reworked/images/"
label_dir = "./reworked/labels/"
output_image_dir = "./augmented/images/"
output_label_dir = "./augmented/labels/"

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

p = Augmentor.Pipeline(image_dir)

p.rotate(probability=0.6, max_left_rotation=5, max_right_rotation=5)
p.zoom(probability=0.5, min_factor=1, max_factor=1.2)
p.shear(probability=0.2, max_shear_left=3, max_shear_right=3)
p.flip_random(probability=0.3)

p.sample(500)