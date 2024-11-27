from typing import List

from src.files import create_file, read_file, add_content_to_file


class Hash:
    def __init__(self):
        self.hashes = []

    def contains(self, hash_s: str) -> bool:
        return hash_s in self.hashes

    def add(self, hash_s: str):
        self.hashes.append(hash_s)

    def read_from_file(self, file_path: str):
        content = read_file(file_path)
        self.hashes = content.split("\n")

    def save_to_file(self, file_path: str):
        create_file(file_path, "\n".join(self.hashes))

    def add_last_to_file(self, file_path: str):
        add_content_to_file(file_path, self.hashes[-1] + "\n")


