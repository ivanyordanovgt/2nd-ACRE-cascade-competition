import time

import cv2
from extract_mask import apply_hsv_mask

def draw_yolo_boxes(image_path, yolo_txt_path, output_path="draw_test.png", rework_img=False):
    if rework_img:
        image = apply_hsv_mask(image_path, False)
    else:
        image = cv2.imread(image_path)

    height, width, _ = image.shape
    with open(yolo_txt_path, 'r') as file:
        boxes = file.readlines()

    for box in boxes:
        class_id, x_center, y_center, bbox_width, bbox_height = map(float, box.split())
        x_center, bbox_width = x_center * width, bbox_width * width
        y_center, bbox_height = y_center * height, bbox_height * height

        x_min = int(x_center - (bbox_width / 2))
        y_min = int(y_center - (bbox_height / 2))
        x_max = int(x_center + (bbox_width / 2))
        y_max = int(y_center + (bbox_height / 2))

        for img in [image, image]:
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(img, str(int(class_id)), (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imwrite(output_path, image)

img_path = r'D:\brawl-stars-ai-training\dataset\test\images\40_aug_0.jpg'
annotations_path = r"D:\brawl-stars-ai-training\dataset\test\labels\40_aug_0.txt"
draw_yolo_boxes(img_path, annotations_path)
