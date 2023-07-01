import numpy as np
import cv2

def create_black_image(width: int = 128, height: int = 128):
    # create a black image
    img = np.zeros((width, height, 3), dtype=np.uint8)
    img = cv2.resize(img, (128, 128))
    # convert the images to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def create_dark_image(width: int = 128, height: int = 128):
    # create a black image
    img = np.random.randint(10, size=(width, height, 3), dtype=np.uint8)
    img = cv2.resize(img, (128, 128))
    # convert the images to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img