import os
import cv2
from smart_farm_robotix.extract_mask import apply_hsv_mask
from smart_farm_robotix.xml_to_yolo import parse_xml_to_yolo

folder_path = '../given_datasets/data/Bean/2022-06-08-16-09'

jpg_files = []
xml_files = []
COLOR_REMOVAL_ALGORITHM = False

for filename in os.listdir(folder_path):
    if filename.endswith('.jpg'):
        jpg_files.append(os.path.join(folder_path, filename))
    elif filename.endswith('.xml'):
        xml_files.append(os.path.join(folder_path, filename))

for i in range(len(jpg_files)):
    if COLOR_REMOVAL_ALGORITHM:
        result_image = apply_hsv_mask(jpg_files[i], None)
    else:
        result_image = cv2.imread(jpg_files[i])

    yolo_data = parse_xml_to_yolo(xml_files[i])[0]
    with open(f"./labels/{i}.txt", 'w') as file:
        file.write("\n".join(yolo_data))

    cv2.imwrite(f"./images/{i}.jpg", result_image)
