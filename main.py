from pathlib import Path

import cv2
import numpy as np


SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png"}

STYLE_SETTINGS = {
    1: {
        "name": "Soft Cartoon",
        "sigma_s": 150,
        "sigma_r": 0.25,
        "edge_strength": 1,
    },
    2: {
        "name": "Bold Cartoon",
        "sigma_s": 60,
        "sigma_r": 0.5,
        "edge_strength": 2,
    },
    3: {
        "name": "Classic Cartoon",
        "sigma_s": 80,
        "sigma_r": 0.35,
        "edge_strength": 3,
    },
}


def load_image(image_path):
    """Load and validate the input image."""
    cleaned_path = image_path.strip().strip('"').strip("'")
    path = Path(cleaned_path).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported image format. Use JPG, JPEG, or PNG.")

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(f"Unable to read the image: {path}")

    return image, path


def create_classic_cartoon(image):
    """Create a cartoon effect using smoothing, colour reduction and edges."""
    smoothed = cv2.bilateralFilter(image, 9, 75, 75)

    data = np.float32(smoothed).reshape((-1, 3))
    criteria = (
        cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,
        20,
        1.0,
    )

    _, labels, centres = cv2.kmeans(
        data,
        8,
        None,
        criteria,
        5,
        cv2.KMEANS_PP_CENTERS,
    )

    centres = np.uint8(centres)
    quantised = centres[labels.flatten()]
    quantised = quantised.reshape(smoothed.shape)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)

    edges = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        7,
    )

    return cv2.bitwise_and(quantised, quantised, mask=edges)


def apply_cartoon_style(image, style):
    """Apply the selected cartoon style."""
    if style not in STYLE_SETTINGS:
        raise ValueError("Style must be 1, 2, or 3.")

    settings = STYLE_SETTINGS[style]

    if style == 3:
        return create_classic_cartoon(image)

    return cv2.stylization(
        image,
        sigma_s=settings["sigma_s"],
        sigma_r=settings["sigma_r"],
    )


def save_image(image, input_path, style):
    """Save the cartoon image beside the original image."""
    style_name = STYLE_SETTINGS[style]["name"].lower().replace(" ", "_")
    output_name = f"{input_path.stem}_cartoon_{style_name}.png"
    output_path = input_path.parent / output_name

    if not cv2.imwrite(str(output_path), image):
        raise OSError(f"Unable to save the output image: {output_path}")

    return output_path


def display_image(image, title):
    """Display the result in a window sized for the screen."""
    display_image = image.copy()

    screen_width = 1200
    screen_height = 800

    height, width = display_image.shape[:2]

    scale = min(
        screen_width / width,
        screen_height / height,
        1.0,
    )

    if scale < 1:
        new_size = (
            int(width * scale),
            int(height * scale),
        )
        display_image = cv2.resize(
            display_image,
            new_size,
            interpolation=cv2.INTER_AREA,
        )

    cv2.imshow(title, display_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_style():
    """Ask the user to choose a cartoon style."""
    while True:
        print("\nChoose a cartoon style:")
        print("1. Soft cartoon")
        print("2. Bold cartoon")
        print("3. Classic cartoon")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice in {"1", "2", "3"}:
            return int(choice)

        if choice == "4":
            return None

        print("Invalid choice. Please select 1, 2, 3, or 4.")


def main():
    print("=" * 45)
    print("           OPENCV CARTOONIFY")
    print("=" * 45)

    image_path = input(
        "\nEnter the path of the image you want to cartoonify: "
    ).strip()

    try:
        image, input_path = load_image(image_path)
    except (FileNotFoundError, ValueError) as error:
        print(f"\nError: {error}")
        return

    style = get_style()

    if style is None:
        print("\nOperation cancelled.")
        return

    try:
        cartoon_image = apply_cartoon_style(image, style)

        output_path = save_image(
            cartoon_image,
            input_path,
            style,
        )

        print("\nCartoon image saved to:")
        print(output_path)

        display_image(
            cartoon_image,
            STYLE_SETTINGS[style]["name"],
        )

    except (ValueError, OSError, cv2.error) as error:
        print(f"\nProcessing error: {error}")


if __name__ == "__main__":
    main()
    