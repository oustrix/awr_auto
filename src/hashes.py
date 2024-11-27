from typing import List

from src.files import read_file, add_content_to_file, overwrite_file


class Hash:
    def __init__(self):
        self.hashes = {}

    def contains(self, hash_s: str) -> bool:
        if hash_s in self.hashes:
            self.hashes[hash_s] = True

        return hash_s in self.hashes

    def add(self, hash_s: str):
        if not self.contains(hash_s):
            self.hashes[hash_s] = True

    def read_from_file(self, file_path: str):
        content = read_file(file_path)
        self.hashes = {hash_s: False for hash_s in content.split("\n")}

    def save_to_file(self, file_path: str):
        overwrite_file(
            file_path,
            "\n".join([hash_s for hash_s in self.hashes if self.hashes[hash_s]]),
        )

    def add_to_file(self, file_path: str, hash_s: str):
        add_content_to_file(file_path, hash_s)
        if not self.contains(hash_s):
            self.hashes[hash_s] = True
