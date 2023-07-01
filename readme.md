# CompareImages

CompareImages is a command-line tool that allows you to compare images using various algorithms. You can compare images within a folder or compare them to a black or dark frame.

## Prerequisites

- Python 3.6 or higher

## Installation

1. Clone the repository:

```shell
git clone git@github.com:AdrienLF/ImageComparison.git
cd compare-images
```
2. Install the required dependencies:

```shell
pip install -r requirements.txt
```

## Usage

````shell
python CompareImages.py --img-folder <path_to_folder> [--to-black] [--to-dark] [--dark-threshold <threshold>]
````

Replace `<path_to_folder>` with the actual path to the folder containing the images you want to compare. Use the optional flags --to-black and/or `--to-dark` to enable the respective comparison options. The `--dark-threshold` option allows you to set a custom threshold value for the dark frame comparison (default is 10).

## Examples

1. Compare images within a folder:
```shell
python CompareImages.py --img-folder img/
```

#### Example output:
````
Comparing credits1.jpg with credits2.jpg:
    ssim = 0.3587869243964623 (Higher means identical)
    mse = 14.930908203125 (Lower means identical)
    rootsift = 21 (Matches between images)
    credits1.jpg borders black = False
    credits1.jpg borders dark = False

0.3587869243964623 21 14.930908203125 False False
````

2. Compare images to a black frame:
````shell
python CompareImages.py --img-folder img/ --to-black
````

#### Example output:
```
Comparing black with credits1.jpg:
            ssim = 0.3587869243964623 (Higher means identical)
            mse = 14.930908203125 (Lower means identical)
            rootsift = 21 (Matches between images)
            black borders black = False
            black borders dark = False
            
0.3587869243964623 21 14.930908203125 False False
```

3. Compare images to a dark frame with a custom threshold:
```shell
python CompareImages.py --img-folder img/ --to-dark --dark-threshold 20
```

#### Example output
```
Comparing dark (threshold = 20) with credits1.jpg:
            ssim = 0.18999967343675722 (Higher means identical)
            mse = 19.7728271484375 (Lower means identical)
            rootsift = 0 (Matches between images)
            dark (threshold = 20) borders black = False
            dark (threshold = 20) borders dark = True
            
0.18999967343675722 0 19.7728271484375 False True
```
# Algorithms
The following algorithms are used for image comparison:

`SSIM`: Structural Similarity Index. Returns a float between 0 and 1, where 1 means the images are identical.

`RootSIFT`: Calculates the number of matches between images.

`MSE`: Mean Squared Error. Returns the difference between images using the Mean Squared Error metric.

`Borders`: Compares the borders of the images to either black or a dark frame.

# License
This project is licensed under the MIT License.