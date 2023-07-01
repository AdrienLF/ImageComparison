import cv2
from pathlib import Path
import numpy as np

def preprocess_image(img, grayscale=True):
    # load the input images
    if type(img) is not np.ndarray:
        if Path(img).is_file():
            img = cv2.imread(img)
    else:
        grayscale = False

    img1 = cv2.resize(img, (128, 128))
    # convert the images to grayscale
    if grayscale:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    return img1
