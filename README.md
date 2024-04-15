# Image Alignment Script

This script aligns a set of source images with a reference destination image using ORB feature detection and homography estimation.

## Requirements
- Python 3.x
- OpenCV (`cv2` module)
- NumPy
- argparse (standard library)

## Usage

### Running the Script
1. Clone or download the script to your local machine.
2. Ensure you have the required dependencies installed.
3. Open a terminal or command prompt.
4. Navigate to the directory containing the script.

   ```
   cd /path/to/script/directory
   ```

5. Run the script with the desired options:

   ```
   python image_alignment.py --sourceFolder /path/to/source/images --dstImage /path/to/destination/image --outputdir /path/to/save/images
   ```

### Command Line Arguments

- `--sourceFolder`: Path to the source folder containing images to be aligned. Default is set to "input" folder in the script directory.
- `--dstImage`: Path to the reference destination image to which the source images will be aligned. Default is set to "ref-image/reference.jpg" in the script directory.
- `--outputdir`: Path to the directory where aligned images will be saved. Default is set to "output" folder in the script directory.

### Supported Image Formats
The script supports the following image formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`.

## Output
- Aligned images will be saved in the specified output directory.
- A visualization of the aligned image will be displayed momentarily for each processed image.

## Note
- Ensure that the source images and the destination image are of compatible sizes and orientations for accurate alignment.
