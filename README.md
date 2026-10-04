# OpenCV Cartoonify

A Python-based image cartoonification tool built with OpenCV. It converts JPG, JPEG, and PNG images into cartoon-style artwork using multiple image-processing techniques.

## Features

- Convert JPG, JPEG, and PNG images into cartoon-style artwork
- Three different cartoon styles
- Soft Cartoon style
- Bold Cartoon style
- Classic Cartoon style
- Classic Cartoon style combines colour reduction and edge detection
- Supports Windows file paths with or without quotation marks
- Automatically saves the processed image beside the original
- Preserves the original image resolution when saving
- Automatically scales large images for comfortable preview
- Input validation with clear error messages
- Simple command-line interface

## Cartoon Styles

### 1. Soft Cartoon

Uses OpenCV's stylization filter with stronger smoothing to create a soft artistic cartoon effect.

### 2. Bold Cartoon

Uses a different OpenCV stylization configuration to produce a stronger and more defined artistic effect.

### 3. Classic Cartoon

Creates a traditional cartoon-like effect by combining:

- Bilateral filtering
- Colour reduction using K-means clustering
- Grayscale conversion
- Adaptive thresholding
- Edge detection

This produces simplified colours with defined outlines.

## Requirements

- Python 3.8 or newer
- OpenCV
- NumPy

## Installation

Clone the repository:

    git clone https://github.com/RaavanHrishi07/OpenCV-Cartoonify.git

Move into the project directory:

    cd OpenCV-Cartoonify

Install the required dependencies:

    pip install -r requirements.txt

## Usage

Run the application:

    python main.py

Enter the path of the image when prompted.

Example:

    Enter the path of the image you want to cartoonify:
    D:\Images\photo.jpg

The program will then display the available styles:

    Choose a cartoon style:
    1. Soft cartoon
    2. Bold cartoon
    3. Classic cartoon
    4. Exit

Select the desired style and the program will process the image.

The resulting cartoon image is automatically saved in the same directory as the original image.

Example output:

    photo_cartoon_soft_cartoon.png

## How It Works

1. The program asks the user to provide an image path.
2. The image path and file format are validated.
3. The image is loaded using OpenCV.
4. The user selects one of the available cartoon styles.
5. The selected image-processing technique is applied.
6. The processed image is saved as a PNG file.
7. The cartoon image is displayed as a preview.

## Project Structure

    OpenCV-Cartoonify/
    │
    ├── main.py
    ├── requirements.txt
    ├── .gitignore
    ├── README.md
    └── LICENSE

## Technologies Used

- Python
- OpenCV
- NumPy

## Supported Image Formats

The application currently supports:

- JPG
- JPEG
- PNG

## Output

Processed images are saved automatically in the same directory as the input image.

The original image is not modified.

## Error Handling

The application validates:

- Whether the image exists
- Whether the provided path points to a file
- Whether the image format is supported
- Whether OpenCV can successfully read the image
- Whether a valid cartoon style has been selected
- Whether the processed image can be saved

## Author

**Hrishikesh Sharma**

GitHub: https://github.com/RaavanHrishi07

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.