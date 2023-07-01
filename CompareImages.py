import argparse
import itertools
from pathlib import Path
import generate_images
import image_tools


class ComparisonError(Exception):
    def __init__(self):
        print("Can't compare to black and to dark, choose one")


class CompareImages():
    """Given a folder of images, compare images together using a variety of algorithms.
    Can also compare each image to either black or a dark monochrome frame."""

    def __init__(self, img_folder: Path, to_black=False, to_dark=False, dark_threshold: int = 10):
        self.img_folder = img_folder
        self.files = self.get_all_image_files()
        self.to_black = to_black
        self.to_dark = to_dark
        self.dark_threshold = dark_threshold

        if self.to_dark and self.to_black:
            raise ComparisonError()

    def get_all_image_files(self):
        image_folder = Path(self.img_folder)
        img_files = sorted([file.as_posix() for file in image_folder.iterdir()])
        print(img_files)
        return img_files

    def ssim(self, img_file1, img_file2):
        """
        Returns float between 0 and 1. 1 means images are identical.
        """
        from skimage.metrics import structural_similarity as ssim
        img1 = image_tools.preprocess_image(img_file1)
        img2 = image_tools.preprocess_image(img_file2)
        return ssim(img1, img2)

    def rootSIFT(self, img_file1, img_file2):
        """
        Returns number of matches between images.
        Number of matches depends on image complexity, so identical but simple images can return low matches
        """
        from comparison_algo.RootSIFT import calc_rootSIFT
        img1 = image_tools.preprocess_image(img_file1)
        img2 = image_tools.preprocess_image(img_file2)

        matches = calc_rootSIFT(img1, img2)
        return len(matches)

    def mse(self, img_file1, img_file2):
        """
        Returns MSE difference between images.
        Smaller means images are closer together.
        """
        from comparison_algo.mse import mse
        img1 = image_tools.preprocess_image(img_file1)
        img2 = image_tools.preprocess_image(img_file2)

        error, diff_array = mse(img1, img2)
        return error

    def compare_borders_to_black(self, img_file1, border_size: int = 10):
        """
        Returns true if the image borders are full black.
        """
        from comparison_algo import image_borders
        file = image_tools.preprocess_image(img_file1, grayscale=False)

        left, right = image_borders.extract_left_right_borders(file, border_size)

        full_black = False
        if image_borders.is_array_empty(left) and image_borders.is_array_empty(right):
            full_black = True

        return full_black

    def compare_borders_to_dark(self, img_file1, border_size: int = 10, dark_threshold: int = 10):
        """
        Returns true if the image borders are darker than threshold.
        """
        from comparison_algo import image_borders
        file = image_tools.preprocess_image(img_file1, grayscale=False)

        left, right = image_borders.extract_left_right_borders(file, border_size)

        dark = False
        if image_borders.is_array_dark(left, dark_threshold) and image_borders.is_array_dark(right, dark_threshold):
            dark = True

        return dark

    def every_algo(self, img_file1, img_file2):
        ssim = self.ssim(img_file1, img_file2)
        rootsift = self.rootSIFT(img_file1, img_file2)
        mse = self.mse(img_file1, img_file2)
        black = self.compare_borders_to_black(img_file1, border_size=10)
        dark = self.compare_borders_to_dark(img_file1, border_size=10, dark_threshold=10)

        return ssim, rootsift, mse, black, dark

    def compare(self):
        for file, file2 in itertools.pairwise(self.files):
            filenames = Path(file).name, Path(file2).name

            if self.to_black:
                black_img = generate_images.create_black_image()
                img1 = black_img
                img2 = file
                filenames = "black", Path(file).name

            if self.to_dark:
                dark_img = generate_images.create_dark_image()
                img1 = dark_img
                img2 = file
                filenames = f"dark (threshold = {self.dark_threshold})", Path(file).name

            else:
                img1 = file
                img2 = file2

            ssim, rootsift, mse, black, dark = self.every_algo(img1, img2)
            print(f"""Comparing {filenames[0]} with {filenames[1]}:
            ssim = {ssim} (Higher means identical)
            mse = {mse} (Lower means identical)
            rootsift = {rootsift} (Matches between images)
            {filenames[0]} borders black = {black}
            {filenames[0]} borders dark = {dark}
            """)
            yield ssim, rootsift, mse, black, dark


def main():
    parser = argparse.ArgumentParser(description="CompareImages - Compare images using various algorithms.")
    parser.add_argument("--img-folder", required=True, help="Folder containing images to compare.")
    parser.add_argument("--to-black", action="store_true", help="Compare images to a black frame.")
    parser.add_argument("--to-dark", action="store_true", help="Compare images to a dark frame.")
    parser.add_argument("--dark-threshold", type=int, default=10, help="Threshold for dark frame comparison.")

    args = parser.parse_args()

    img_folder = Path(args.img_folder)
    for ssim, rootsift, mse, black, dark in CompareImages(img_folder, args.to_black, args.to_dark,
                                                         args.dark_threshold).compare():
        print(ssim, rootsift, mse, black, dark)


if __name__ == '__main__':
    main()
