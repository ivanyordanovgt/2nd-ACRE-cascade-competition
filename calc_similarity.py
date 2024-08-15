import numpy as np
import cv2

from utils.annotations import read_annotations


def bb_intersection_over_union(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    interArea = max(0, xB - xA) * max(0, yB - yA)
    boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
    boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
    iou = interArea / float(boxAArea + boxBArea - interArea)
    return iou



def evaluate_detections(detections, file_path, iou_threshold=0.1):
    image_width, image_height = 2046, 1080
    annotations = read_annotations(file_path, image_width, image_height)
    matches = 0
    used_annotations = np.zeros(len(annotations))

    for det in detections:
        x1, y1, x2, y2, _ = det
        for i, anno in enumerate(annotations):
            if used_annotations[i] == 0:
                iou = bb_intersection_over_union((x1, y1, x2, y2), anno)
                if iou >= iou_threshold:
                    matches += 1
                    used_annotations[i] = 1
                    break

    max_possible_matches = max(len(detections), len(annotations))
    similarity_percentage = (matches / max_possible_matches) * 100 if max_possible_matches > 0 else 0
    return similarity_percentage
