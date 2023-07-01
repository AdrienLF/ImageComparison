from pathlib import Path
import itertools
from time import time
from image_tools import preprocess_image
import numpy as np
from matplotlib import pyplot as plt
np.set_printoptions(threshold=np.inf)

def extract_image_borders(image, size):
    height, width = image.shape[:2]
    top, bottom, left, right = size, height - size, size, width - size
    border = image[top:bottom, left:right]
    return border

def extract_left_right_borders(image, size):
    left_border = image[:, :size]
    right_border = image[:, -size:]
    return left_border, right_border

def extract_middle_frame(image, frame_width, frame_height):
    height, width = image.shape[:2]
    start_row = (height - frame_height) // 2
    end_row = start_row + frame_height
    start_col = (width - frame_width) // 2
    end_col = start_col + frame_width
    frame = image[start_row:end_row, start_col:end_col]
    return frame

def is_array_empty(array):
    """
    If array is empty, it could mean it's a black image if it's a full image,
    OR that the cropped image is black. Useful to check if it's a credits scene.
    """
    return np.all(array == 0)

def is_array_dark(arr, threshold:int = 10):
    return np.all(np.logical_and(arr >= 0, arr < threshold))

if __name__ == '__main__':
    img_folder = Path("../img")
    img_files = sorted([file.as_posix() for file in img_folder.iterdir()])
    for file, file2 in itertools.pairwise(img_files):
        print(file)
        file = preprocess_image(file, grayscale=False)
        # plt.imshow(file, interpolation='nearest')
        # plt.show()
        file2 = preprocess_image(file2, grayscale=False)

        now = time()
        # Specify the size of the border in pixels
        border_size = 10

        # Extract the borders of the image
        left, right = extract_left_right_borders(file, 3)
        # plt.imshow(left, interpolation='nearest')
        # plt.show()

        # Print the extracted border
        #print(left)
        print(f"Array black = {is_array_empty(left)}")
        print(f"Array dark = {is_array_dark(left, 10)}")
        print(f"Highest value = {np.amax(left)}")
        print(f"Unique values in array = {np.unique(left)}")

        time_spent = time() - now
        print(f"Time took for 1 comparison: {time_spent}")
