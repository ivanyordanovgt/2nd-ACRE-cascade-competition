import os
import random
from PIL import Image

from smart_farm_robotix.utils.annotations import load_yolo_annotations, yolo_to_bbox, is_position_valid, \
    bbox_to_yolo
from smart_farm_robotix.utils.file_operations import get_paths_from_folder
from utils.file_operations import crop_object_in_transparent_img

class Count:

    def __init__(self):
        self.count = 0

    def add(self, num=1):
        self.count += num


def augment_image_with_assets(image_path, label_path, assets, output_images_dir, output_labels_dir,
                              count, num_augmentations=10):
    img = Image.open(image_path)
    img_width, img_height = img.size
    annotations = load_yolo_annotations(label_path)

    existing_bboxes = [yolo_to_bbox(ann, img_width, img_height) for ann in annotations]

    for i in range(random.randint(1, 2)):
        augmented_img = img.copy()
        new_annotations = annotations.copy()
        count.add()
        if count.count >= 50:
            return False
        for _ in range(random.randint(3, 10)):
            asset = random.choice(assets)
            asset_img = Image.open(asset)
            asset_img = crop_object_in_transparent_img(asset_img)
            asset_img = asset_img.rotate(random.randint(0, 365))

            asset_width, asset_height = asset_img.size

            valid_position = False
            for _ in range(100):
                x = random.randint(0, img_width - asset_width)
                y = random.randint(0, img_height - asset_height)
                asset_bbox = (x, y, x + asset_width, y + asset_height)

                if is_position_valid(asset_bbox, existing_bboxes, img_width, img_height):
                    valid_position = True
                    break

            if valid_position:
                augmented_img.paste(asset_img, (x, y), asset_img)
                new_annotations.append(bbox_to_yolo(asset_bbox, img_width, img_height))
                existing_bboxes.append(asset_bbox)

        base_name = os.path.basename(image_path).split('.')[0]
        augmented_img_name = f"{base_name}_aug_{i}.jpg"
        augmented_img_path = os.path.join(output_images_dir, augmented_img_name)
        augmented_img.save(augmented_img_path)

        annotation_name = f"{base_name}_aug_{i}.txt"
        annotation_path = os.path.join(output_labels_dir, annotation_name)
        with open(annotation_path, 'w') as f:
            for ann in new_annotations:

                f.write(f"{ann[0]} {ann[1]:.6f} {ann[2]:.6f} {ann[3]:.6f} {ann[4]:.6f}\n")




dataset_folders = ['test', 'train', 'valid']
assets = get_paths_from_folder("../get_assets/photoshop/", ['.png'])['.png']

output_images_dir = "./reworked/images"
output_labels_dir = "./reworked/labels"

os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_labels_dir, exist_ok=True)
count = Count()
for path in dataset_folders:
    images = get_paths_from_folder(f"D:/brawl-stars-ai-training/dataset/{path}/images", [".jpg"])['.jpg']
    labels = get_paths_from_folder(f"D:/brawl-stars-ai-training/dataset/{path}/labels", [".txt"])['.txt']

    for i in range(len(images)):
        r_index = random.randint(0, len(images) - 1)
        r_img_path = images.pop(r_index)
        r_label_path = labels.pop(r_index)
        augment_image_with_assets(r_img_path, r_label_path, assets, output_images_dir, output_labels_dir, count)
