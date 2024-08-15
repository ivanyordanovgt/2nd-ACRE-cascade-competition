import os
import shutil
import numpy as np

TRAIN_PCT = 0.8
VAL_PCT = 0.1


def split_data(image_dir, label_dir, root_dir, train_pct, val_pct):
    subsets = ['train', 'val', 'test']
    for subset in subsets:
        os.makedirs(os.path.join(root_dir, subset, 'images'), exist_ok=True)
        os.makedirs(os.path.join(root_dir, subset, 'labels'), exist_ok=True)

    images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    labels = [f for f in os.listdir(label_dir) if f.endswith('.txt')]

    images = [img for img in images if img.split('.')[0] + '.txt' in labels]

    np.random.shuffle(images)

    total_images = len(images)
    train_end = int(total_images * train_pct)
    val_end = train_end + int(total_images * val_pct)

    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    def move_files(files, subset):
        for file in files:
            shutil.move(os.path.join(image_dir, file),
                        os.path.join(root_dir, subset, 'images', file))
            shutil.move(os.path.join(label_dir, file.split('.')[0] + '.txt'),
                        os.path.join(root_dir, subset, 'labels', file.split('.')[0] + '.txt'))

    move_files(train_images, 'train')
    move_files(val_images, 'val')
    move_files(test_images, 'test')


split_data('./images', './labels', './', TRAIN_PCT, VAL_PCT)
