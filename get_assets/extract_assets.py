from utils import get_paths_from_folder
import cv2
import os

paths = get_paths_from_folder("./dataset", ['.jpg', '.txt'])


def crop_yolo_annotations(image_path, annotation_path, file_index=0, output_dir='./assets'):
    os.makedirs(output_dir, exist_ok=True)

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"ERROR! {image_path} path is not valid.")

    img_height, img_width = image.shape[:2]

    with open(annotation_path, 'r') as file:
        annotations = file.readlines()

    for idx, annotation in enumerate(annotations):
        _, x_center, y_center, width, height = map(float, annotation.split())

        x_center *= img_width
        y_center *= img_height
        width *= img_width
        height *= img_height

        x_min = int(x_center - width / 2)
        y_min = int(y_center - height / 2)

        x_max = int(x_center + width / 2)
        y_max = int(y_center + height / 2)

        cropped_img = image[y_min:y_max, x_min:x_max]
        output_path = os.path.join(output_dir, f'crop_{file_index}_{idx}.jpg')
        try:
            cv2.imwrite(output_path, cropped_img)
        except:
            print("ERROR. Image couldn't be saved.")

    print(f"Cropped asset saved in: {output_dir}")


jpgs = paths['.jpg']
txts = paths['.txt']

if len(jpgs) != len(txts):
    message = ("!!! WARNING !!! \n"
               "Amount of images do not match with the amount of labels \n"
               "This will result in errors.")

    print(message)

for i in range(len(jpgs)):
    crop_yolo_annotations(jpgs[i], txts[i])
