import os
import codecs

import glob


def create_file(directory: str, file_name: str, content: str = "") -> str:
    """

    :param directory: директория, в которой будет создан файл.
    :param file_name: название создаваемого файла
    :param content: содержимое создаваемого файла[опционально]
    :return: путь к созданному или существующему файлу
    """
    file_path = os.path.join(directory, file_name)

    with open(file_path, "wb") as file:
        file.write(content.encode())

    return file_path


def add_content_to_file(file_path: str, content: str):
    with codecs.open(file_path, "a", "utf-8") as file:
        file.write(content)


def create_directory(path: str) -> str:
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def get_emp_files_in_directory(directory_path: str) -> List[str]:
    emp_files = glob.glob(os.path.join(directory_path, "*.emp"))
    return emp_files
