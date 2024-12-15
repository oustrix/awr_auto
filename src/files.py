import os
import codecs

import glob
from typing import List

import transliterate

def create_file(file_path: str, content: str = "") -> str:
    """
    Создает файл с указанным именем и содержимым в указанной директории.
    """

    with open(file_path, "wb") as file:
        file.write(content.encode())

    return file_path


def read_file(file_path: str) -> str:
    with codecs.open(file_path, "r", "utf-8") as file:
        return file.read()


def overwrite_file(file_path: str, content: str):
    with codecs.open(file_path, "w", "utf-8") as file:
        file.write(content)


def add_content_to_file(file_path: str, content: str):
    with codecs.open(file_path, "a", "utf-8") as file:
        file.write(content)


def create_directory(path: str) -> str:
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def get_emp_files_in_directory(directory_path: str) -> List[str]:
    emp_files = glob.glob(os.path.join(directory_path, "*.emp"), recursive=True)
    return emp_files

def get_cst_files_in_directory(directory_path: str) -> List[str]:
    cst_files = glob.glob(os.path.join(directory_path, "*.cst"), recursive=True)
    return cst_files

def transliterate_filename(filename):
    name, extension = os.path.splitext(filename)

    transliterated_name = transliterate.translit(name, reversed=True)

    return transliterated_name + extension