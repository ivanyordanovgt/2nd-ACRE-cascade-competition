import time
import cv2
import numpy as np


def apply_hsv_mask(image_path, save_path):

    image = cv2.imread(image_path)
    start_time = time.time()

    # lower_hsv = (21, 0, 43) BEST
    # upper_hsv = (105, 139, 255)
    lower_hsv = (31, 11, 43) # TEST
    upper_hsv = (90, 130, 255)
    # reddish_plant_lower = np.array([114, 15, 52])
    # reddish_plant_upper = np.array([179, 68, 160])
    reddish_plant_lower = np.array(lower_hsv)
    reddish_plant_upper = np.array(upper_hsv)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array(lower_hsv)
    upper = np.array(upper_hsv)
    mask_user = cv2.inRange(hsv_image, lower, upper)

    mask_reddish = cv2.inRange(hsv_image, reddish_plant_lower, reddish_plant_upper)

    combined_mask = cv2.bitwise_or(mask_user, mask_reddish)

    result = cv2.bitwise_and(image, image, mask=combined_mask)

    if save_path:
        cv2.imwrite(save_path, result)

    print("TIME TO REWORK IMAGE: ", time.time()-start_time)
    return result


# Define HSV range


# Apply the HSV mask and save the image
# apply_hsv_mask('tested_images/img_first_test.jpg')