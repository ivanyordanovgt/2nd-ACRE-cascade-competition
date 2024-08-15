import numpy as np
from ultralytics import YOLO
import cv2

from calc_similarity import evaluate_detections
from extract_mask import apply_hsv_mask
from utils.file_operations import get_paths_from_folder
from xml_to_yolo import parse_xml_to_yolo


def train(model, epochs=30, imgsz=640):
    if __name__ == "__main__":
        results = model.train(
            data='../dataset/data.yaml',
            epochs=epochs,
            imgsz=imgsz,
            device="cuda",
        )

        return results


def test(model, img_path, color_rework=False):
    img_path = img_path
    if color_rework:
        img = apply_hsv_mask(img_path, False)
        img = np.array(img, dtype=np.uint8)
    else:
        img = cv2.imread(img_path)
    results = model(img, save=False, device="cuda")
    detections = []
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = [int(x) for x in box.xyxy.tolist()[0]]
            class_id = int(box.cls.tolist()[0])
            detections.append([x1, y1, x2, y2, class_id])

    return detections


def evaluate_model_performance(model, TEST_AMOUNT, test_dataset_path):
    files = get_paths_from_folder(f"./given_datasets/data/Bean/2022-06-08-17-24/", [".jpg", ".xml"])
    jpg_files = files['.jpg']
    xml_files = files['.xml']

    total = 0
    for i in range(TEST_AMOUNT):
        test_image_path = jpg_files[i]
        test_label_path = xml_files[i]
        detections = test(model, img_path=test_image_path, color_rework=False)
        yolo_data, image_width, image_height = parse_xml_to_yolo(test_label_path)

        with open("test.txt", 'w') as file:
            file.write("\n".join(yolo_data))

        similarity = evaluate_detections(detections, "./test.txt")
        total += similarity

    result = total / TEST_AMOUNT
    return result

TEST_AMOUNT = 1
train_count = 40
EPOCHS, IMGSZ = 100, 640
TEST_DATASET_PATH = f"./given_datasets/data/Bean/2022-06-08-17-24/"
# model_path = f"./runs/detect/train{train_count}/weights/best.pt"
model_path = "yolov8n.yaml"
model = YOLO(model_path)
train(model, EPOCHS, IMGSZ)
# evaluate_model_performance(model, TEST_AMOUNT, TEST_DATASET_PATH)
