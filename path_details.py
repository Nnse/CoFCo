# Separator
SEPARATOR = '/'


def get_cleaned_path(path: str) -> str:
    # Unified separator
    return path.replace('\\', SEPARATOR)


def get_file_directory(path: str) -> str:
    # Split paths with separators
    separator_split_path = get_cleaned_path(path).split(SEPARATOR)
    # Get all except last
    folder_path = (separator_split_path[:-1])[0]
    return folder_path + SEPARATOR


def get_filename(path: str) -> str:
    # Split paths with separators
    separator_split_path = get_cleaned_path(path).split(SEPARATOR)
    # Get last
    file_last_path = separator_split_path[-1]
    # Remove the extension and take the filename
    filename = file_last_path.split('.')[0]
    return filename


def get_ext(path: str) -> str:
    # Split paths with separators
    separator_split_path = get_cleaned_path(path).split(SEPARATOR)
    # Get last
    file_last_path = separator_split_path[-1]
    # Remove the extension
    ext_name = file_last_path.split('.')[-1]
    # Converted to lower case at the extension for possible JPG, PNG, JPEG
    return ext_name.lower()

