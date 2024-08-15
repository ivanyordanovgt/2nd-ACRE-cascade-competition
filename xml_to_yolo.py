import xml.etree.ElementTree as ET
import os


def parse_xml_to_yolo(xml_file_path):
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML file {xml_file_path}: {e}")
        return [], 0, 0  # Return empty data and dimensions

    image_width = int(root.find('.//size/width').text)
    image_height = int(root.find('.//size/height').text)

    class_map = {'chenopode': 0, 'moutarde': 1, 'haricot': 2}
    data = []

    for clipping in root.findall(".//clippings/clipping"):
        class_name = clipping.find('name').text
        class_id = class_map.get(class_name, -1)
        if class_id == -1:
            continue

        points = [(int(p.get('x')), int(p.get('y'))) for p in clipping.findall('points/point')]
        if not points:
            continue

        x_coords, y_coords = zip(*points)
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        x_center = (x_min + x_max) / 2.0 / image_width
        y_center = (y_min + y_max) / 2.0 / image_height
        bbox_width = (x_max - x_min) / image_width
        bbox_height = (y_max - y_min) / image_height

        data.append(f"{class_id} {x_center} {y_center} {bbox_width} {bbox_height}")

    return data, image_width, image_height

