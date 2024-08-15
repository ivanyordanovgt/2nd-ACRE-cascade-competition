import os

import numpy as np
from PIL import Image


def crop_object_in_transparent_img(image):
    image_array = np.array(image)

    non_transparent_pixels = np.where(image_array[:, :, 3] > 0)

    if not non_transparent_pixels[0].size:
        return image

    min_x = np.min(non_transparent_pixels[1])
    max_x = np.max(non_transparent_pixels[1])
    min_y = np.min(non_transparent_pixels[0])
    max_y = np.max(non_transparent_pixels[0])

    cropped_image = image.crop((min_x, min_y, max_x + 1, max_y + 1))
    return cropped_image

def downscale_image_by_percentage(image, scale_percentage):
    original_width, original_height = image.size
    new_width = int(original_width * (scale_percentage / 100))
    new_height = int(original_height * (scale_percentage / 100))

    # Resize the image using high-quality downsampling
    new_image = image.resize((new_width, new_height), Image.LANCZOS)
    return new_image


def get_paths_from_folder(folder_path, file_types):
    result =  {key: [] for key in file_types}
    for filename in os.listdir(folder_path):
        for file_type in file_types:
            if filename.endswith(file_type):
                result[file_type].append(os.path.join(folder_path, filename))

    return result