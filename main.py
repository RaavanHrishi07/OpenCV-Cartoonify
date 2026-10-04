from pathlib import Path

import cv2


SUPPORTED_FORMATS = {".jpg", ".jpeg", ".png"}


def load_image(image_path):
    """Load an image from a valid file path."""
    cleaned_path = image_path.strip().strip('"').strip("'")
    path = Path(cleaned_path).expanduser()

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if not path.is_file():
        raise ValueError(f"Input path is not a file: {path}")

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(
            "Unsupported image format. Use JPG, JPEG, or PNG."
        )

    image = cv2.imread(str(path))

    if image is None:
        raise ValueError(f"Unable to read the image: {path}")

    return image, path


def apply_cartoon_style(image, style):
    """Apply one of the available cartoon styles."""
    if style == 1:
        return cv2.stylization(
            image,
            sigma_s=150,
            sigma_r=0.25,
        )

    if style == 2:
        return cv2.stylization(
            image,
            sigma_s=60,
            sigma_r=0.5,
        )

    raise ValueError("Style must be 1 or 2.")


def save_image(image, input_path, style):
    """Save the processed image next to the original image."""
    output_name = f"{input_path.stem}_cartoon_style_{style}.png"
    output_path = input_path.parent / output_name

    if not cv2.imwrite(str(output_path), image):
        raise OSError(f"Unable to save the output image: {output_path}")

    return output_path


def display_image(image, title):
    """Display the processed image in an OpenCV window."""
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def get_style():
    """Ask the user to choose a cartoon style."""
    while True:
        print("\nChoose a cartoon style:")
        print("1. Soft cartoon")
        print("2. Bold cartoon")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            return 1

        if choice == "2":
            return 2

        if choice == "3":
            return None

        print("Invalid choice. Please select 1, 2, or 3.")


def main():
    print("=" * 45)
    print("           OPENCV CARTOONIFY")
    print("=" * 45)

    image_path = input(
        "\nEnter the path of the image you want to cartoonify: "
    )

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
            f"Cartoon Style {style}",
        )

    except (ValueError, OSError, cv2.error) as error:
        print(f"\nProcessing error: {error}")


if __name__ == "__main__":
    main()
    