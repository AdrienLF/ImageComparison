from skimage.metrics import structural_similarity as ssim
from pathlib import Path
import itertools
from time import time
from compare_images import preprocess_image

if __name__ == '__main__':
    img_folder = Path("../img")
    img_files = sorted([file.as_posix() for file in img_folder.iterdir()])
    for file, file2 in itertools.pairwise(img_files):
        print(file, file2)
        file = preprocess_image(file)
        file2 = preprocess_image(file2)
        now = time()
        difference = ssim(file, file2)
        print(difference)
        time_spent = time() - now
        print(f"Time took for 1 comparison: {time_spent}")