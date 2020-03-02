# Fourier-Image-Analysis
Short scripts for pre-processing and analyzing images in the context of Fourier Optics.

## File Structure
These scripts read images from and write images to particular subdirectories. For this to function properly, the following file structure is required.

```
project
|
|--- images
|
|--- pinhole
|
|--- transforms
|
| <script_names>.py
```

The `images` subdirectory contains all empirical data; namely, cropped and raw photographs. The programs herein write Fourier transformed images to the `transforms` subdirectory. Images which are Fourier transformed following a simulated low-pass filter are written to the `pinhole` subdirectory. A `cleaned_images` subdirectory is additionally required, if the high-pass filter script is to be used.

## Script Descriptions
The following table lists the scripts found here and summarizes their use. Generally, the list is ordered by importance.

File Name | Function
--- | ---
`fft.py` | Computes the Fast Fourier Transform of an image
`preprocess.py` | Crops an image evenly about its brightest feature, typically in its center
`pinhole.py` | Simulates the effect of a pinhole in the Fourier plane using a low-pass filter
`image_clean.py` | Removes low-frequency background noise via a high-pass filter
`analyze_lines.py` | Computes the rowwise (or column-wise) average pixel values and returns a dataframe
`wavenumber.py` | Converts image pixel units to units of wavenumber 

## Usage
All scripts herein required additional command line arguments to run. Often the only such argument is the full file name of the image undergoing analysis. Furthermore, each script's usage and description can be readily obtained by providing the `--help` flag following the script file name in the command line. The usage for each script follows.

1. `fft.py`

   The only required argument here is the file name of the `image` to be Fourier transformed. Such images are typically raw photographs or result from pre-processing. The `--show` optional flag displays the transformed image for the user before saving the image, while the `--save` flag writes the transformed image, in grayscale format, to the transforms subdirectory.
```
$ python fft.py <image> --show --save
```

2. `preprocess.py`

   The only required argument, again, is the file name of the `image`. This script works by locating the maxima in the row-wise and column-wise averages of pixel value and assigning the corresponding coordinate as the center of the image. Thereafter, the image is cropped about this center. The user may provide the side length is pixels by providing an integer value following the optional `--size` flag. The default value creates a four megapixel (2000 by 2000 pixels) image.
   
   To check that the algorithmically determined center is correct prior to saving, the user may provide the optional `--check` flag which superposes a square about the determined center and prompts the user to continue or abort cropping. The `--show` and `--save` flags respectively display the cropped image and save the cropped image to the images subdirectory.
```
$ python preprocess.py <image> --size SIZE --check --show --save
```

3. `pinhole.py`

   This script requires two arguments, the file name of the `image` and the `diameter` of pinhole in millimeters to be simulated. This script simulates a low-pass filter by masking all pixels not wihtin the given radius of the image's center before Fourier transforming the image. The `--show` and `--save` optional flags resepctively display the filtered image and save the filtered image to the pinhole subdirectory.
```
$ python pinhole.py <image> <diameter> --show --save
```

4. `image_clean.py`

   This script requires only the name of the `image` to be transformed. It functions oppositely to `pinhole.py` by simulating a high-pass filter. To do so, it masks a central square of pixels in the image and Fourier transforms it so that only the high-frequency structure remains. The size of this mask, whose deafult is 5 by 5 pixels, may be changed by providing an integer value following the optional `--mask` flag. The user may also provide the optional `--show` and `--save` flags to reqpectively see the transformed image and save it to the `cleaned_images` subdirectory. Ensure that this directory exists prior to use.
```
$ python image_clean.py <image> --mask MASK --show --save
```

5. `analyze_lines.py`

   This script requires only the name of the `image` to be analyzed. It is particularly useful for images following a lined spatial filter that exhibit an intensity spectrum that varies either vertically or horizontally. The average pixel value of each row (or column) is computed and stored in a Pandas dataframe, which may then be saved as a CSV by providing the optional `--to_csv` flag. The axis on which the average is computed may changed by providing either a 1 or 0 following the optional `--axis` flag. By default, averages are computed row-wise whose axis is 1.
   
   This script's primary use is in conjunction with the `DataVis.R` script which plots its results.
```
$ python analyze_lines.py <image> --to_csv --axis AXIS
```

6. `wavenumber.py`

   This script only requires the name of an `image`. It relabels an image by plotting it with respect to wavenumber units (the reciprocal of length), which are useful for determining the frequencies of different image components. Note that this is only useful for images taken in the Fourier plane. A red grid can be imposed on the image by providing the optional `--grid` flag, but this is often compromised by the limited resolution of the figure. Finally, the `--show` and `--save` optional flags are respectively used to display the figure and save it to the current directory. 
```
$ python wavenumber.py <image> --grid --show --save
```

### Data Visualization in R
A R script is provided to process the output of the `analyze_lines.py` script discussed above. It does not access its resultant CSV file, but rather accesses the Pandas dataframe directly through R's Reticulate package, which offers cross-compatibility between the two. Here, normalized intensity is plotted with respect to the pixel, whose domain can be changed internally.
