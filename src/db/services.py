def convert_to_binary(file_path):
    """
    Convert an image file to binary data.

    :param file_path: Path to the image file
    :return: Binary data of the image
    """
    try:
        with open(file_path, "rb") as file:
            return file.read()
    except (FileNotFoundError, IOError) as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def write_to_file(binary_data, output_path):
    """
    Write binary data to an image file.

    :param binary_data: Binary data to write
    :param output_path: Path to save the image file
    """
    if binary_data is None:
        print("No data to write.")
        return

    try:
        with open(output_path, "wb") as file:
            file.write(binary_data)
    except IOError as e:
        print(f"Error writing to file {output_path}: {e}")
