def load_yolo_annotations(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    annotations = []
    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center = float(parts[1])
        y_center = float(parts[2])
        width = float(parts[3])
        height = float(parts[4])
        annotations.append((class_id, x_center, y_center, width, height))
    return annotations


def yolo_to_bbox(yolo_annotation, img_width, img_height):
    _, x_center, y_center, width, height = yolo_annotation
    xmin = int((x_center - width / 2) * img_width)
    xmax = int((x_center + width / 2) * img_width)
    ymin = int((y_center - height / 2) * img_height)
    ymax = int((y_center + height / 2) * img_height)
    return (xmin, ymin, xmax, ymax)


def bbox_to_yolo(bbox, img_width, img_height):
    xmin, ymin, xmax, ymax = bbox
    x_center = (xmin + xmax) / 2.0 / img_width
    y_center = (ymin + ymax) / 2.0 / img_height
    width = (xmax - xmin) / img_width
    height = (ymax - ymin) / img_height
    return (0, x_center, y_center, width, height)


def is_position_valid(bbox, existing_bboxes, img_width, img_height):
    for existing_bbox in existing_bboxes:
        if (bbox[0] < existing_bbox[2] and bbox[2] > existing_bbox[0] and
                bbox[1] < existing_bbox[3] and bbox[3] > existing_bbox[1]):
            return False
    if bbox[0] < 0 or bbox[1] < 0 or bbox[2] > img_width or bbox[3] > img_height:
        return False
    return True


def read_annotations(file_path, image_width, image_height):
    annotations = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 5:
                x_center = float(parts[1]) * image_width
                y_center = float(parts[2]) * image_height
                width = float(parts[3]) * image_width
                height = float(parts[4]) * image_height
                x1 = x_center - (width / 2)
                y1 = y_center - (height / 2)
                x2 = x_center + (width / 2)
                y2 = y_center + (height / 2)
                annotations.append((x1, y1, x2, y2))
    return annotations
