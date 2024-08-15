## Guide on how to use 

### Reformat dataset

You can reformat the dataset into YOLOv8 format from [reformat.py](https://github.com/ivanyordanovgt/smart_farm_robotix/blob/master/reformat_dataset/reformat.py).

1. Enter the path of the dataset you want to reformat
2. If you want to apply color removal algorithm set ```COLOR_REMOVAL_ALGORITHM``` to ```True```
3. Run
4. Data will be saved inside folders `images` and `labels`

To split the dataset in train/val/valid you should use [split_dataset.py](https://github.com/ivanyordanovgt/smart_farm_robotix/blob/master/reformat_dataset/split_dataset.py)<br>
Set `TRAIN_PERCENTAGE/VAL_PERCENTAGE` or use the default ones.

### Check annotations
To be sure the dataset is converted correctly you can check the new annotations using [draw_yolo_boxes.py](https://github.com/ivanyordanovgt/smart_farm_robotix/blob/master/draw_yolo_boxes.py).<br>
Set `img_path` and `annotations_path` and run the file.<br>
Default output is `draw_test.png`. You can choose the output by passing a param `output_path`.

### Test color removal

1. Go to [extract_mask.py](https://github.com/ivanyordanovgt/smart_farm_robotix/blob/master/extract_mask.py)
2. Enter the params `image_path` and `save_path`
3. Run
4. You can use `draw_yolo_boxes.py` to check if the objects are still visible after the change.

### Get extra assets
The attempt with this one was to extract some of the present assets and tweak them to get some extra examples. You can see how it looks like at<br>
[get_assets](https://github.com/ivanyordanovgt/smart_farm_robotix/tree/master/get_assets)

### Improve dataset
Dataset generator which makes new examples of existing ones by pasting the assets extracted from `get_assets`. This proved to not be very effective.<br>
To use:

1. Go to [generator.py](https://github.com/ivanyordanovgt/smart_farm_robotix/blob/master/improve_dataset/generator.py)
2. Run
3. Data will be saved in `./reworked/`

### YOLO Operations
Here you can test/train/validate the models. 

1. Go to [YOLO_operations.py](https://github.com/ivanyordanovgt/smart_farm_robotix/blob/master/YOLO_operations.py)
2. Enter the model path which you want to use. Enter the `epochs` and `imgsz`. If you do not have a model use "yolov8n.yaml" or "yolov8n.pt" for the path.
3. For training use the function `train` by passing the `model`, `epochs`, `imgsz`.
4. For testing use `evaluate_model_performance` by passing the `model` and `TEST AMOUNT` which is the amount of images you want to perform the test on from the dataset.
