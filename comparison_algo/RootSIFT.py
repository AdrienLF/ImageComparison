# import the necessary packages
import itertools
from time import time
import numpy as np
import cv2
from pathlib import Path


class RootSIFT:
    def __init__(self):
        # initialize the SIFT feature extractor
        self.extractor = cv2.DescriptorExtractor_create("SIFT")

    def compute(self, image, kps, eps=1e-7):
        # compute SIFT descriptors
        (kps, descs) = self.extractor.compute(image, kps)
        # if there are no keypoints or descriptors, return an empty tuple
        if len(kps) == 0:
            return ([], None)
        # apply the Hellinger kernel by first L1-normalizing and taking the
        # square-root
        descs /= (descs.sum(axis=1, keepdims=True) + eps)
        descs = np.sqrt(descs)
        # descs /= (np.linalg.norm(descs, axis=1, ord=2) + eps)
        # return a tuple of the keypoints and descriptors
        return (kps, descs)

def calc_rootSIFT(img1, img2):
    sift = cv2.SIFT_create()

    keypoints_1, descriptors_1 = sift.detectAndCompute(img1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(img2, None)

    # feature matching
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

    matches = bf.match(descriptors_1, descriptors_2)
    matches = sorted(matches, key=lambda x: x.distance)
    #print(len(matches)) # more matches : more similar
    return matches

if __name__ == '__main__':
    img_folder = Path("../img")
    img_files = sorted([file.as_posix() for file in img_folder.iterdir()])
    for file, file2 in itertools.pairwise(img_files):
        print(file, file2)
        now = time()
        img1 = cv2.imread(file)
        img2 = cv2.imread(file2)

        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        matches = calc_rootSIFT(img1, img2)
        time_spent = time()-now
        print(f"Time took for 1 comparison: {time_spent}")