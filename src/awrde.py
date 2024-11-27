import os
import time
from typing import List

import pywinauto
from PIL import Image
from pyawr_utils import awrde_utils
from pywinauto import mouse
from pywinauto.keyboard import send_keys

from src.files import (
    get_emp_files_in_directory,
    create_directory,
    create_file,
    add_content_to_file,
    read_file,
)
from src.hashes import Hash
from src.settings import settings
from src.tags import create_tags

import hashlib


class Awrde:
    def __init__(self):
        self.awrde: awrde_utils.Project = awrde_utils.Project(
            awrde=awrde_utils.establish_link()
        )
        self.is_first_run: bool = True
        self.is_first_graph_opened: bool = False
        self.app_window: pywinauto.WindowSpecification = None
        self.current_file_window = None
        self.output_dir = settings.output_directory_path
        self.input_dir = settings.input_directory_path

    def start_processing(self):
        time.sleep(5)

        files = get_emp_files_in_directory(self.input_dir)

        self.process_files(files)

    def process_files(self, files: List[str]):
        hashed_files = Hash()

        hash_path = os.path.join(self.input_dir, "hashes.txt")
        try:
            hashed_files.read_from_file(hash_path)
        except FileNotFoundError:
            print("Hashes file not found")
            create_file(hash_path, "")

        print(f"Opened hashes file: {hash_path}")

        for file in files:
            file_hash = hashlib.sha256(open(file, "rb").read()).hexdigest()

            if hashed_files.contains(file_hash):
                print(f"Skipping {file}")
                continue

            self.process_file(file)

            hashed_files.add(file_hash)
            hashed_files.add_last_to_file(hash_path)

            print(f"Processed {file}")

        hashed_files.save_to_file(hash_path)

    def process_file(self, file: str):
        self.simulate_file(file)

        if self.is_first_run:
            self.app_window = pywinauto.Application(backend="uia").connect(
                title_re=".*.emp"
            )
            self.is_first_run = False

        self.current_file_window = self.app_window.window(
            title_re=".*.emp", control_type="Window"
        )

        file_name = os.path.basename(file)[:-4]

        self.create_md_file(file_name)

        self.open_graphs_tree()

        self.process_graphs(file_name)

    def simulate_file(self, file: str):
        self.awrde.open_project(file)
        self.awrde.simulate_analyze()

    def open_graphs_tree(self):
        graphs = self.current_file_window.child_window(title="Graphs")
        if len(graphs.sub_elements()) == 0:
            coords = graphs.rectangle().mid_point()
            mouse.double_click(coords=(coords.x, coords.y))

    def process_graphs(self, file_name: str):
        create_directory(f"{self.output_dir}\\{file_name}")

        for graph in self.awrde.graph_name_list:
            screenshot = self.process_graph(graph)

            self.save_screenshot(file_name, graph, screenshot)

    def process_graph(self, name: str) -> Image:
        self.open_graph(name)

        return self.screenshot_graph(name)

    def open_graph(self, name: str):
        coords = (
            self.current_file_window.window(title="Graphs")
            .window(title=name)
            .rectangle()
            .mid_point()
        )
        mouse.double_click(coords=(coords.x, coords.y))

        if not self.is_first_graph_opened:
            try:
                self.app_window.window(title_re=".*.emp", control_type="Window").window(
                    title=name, control_type="Window"
                ).child_window(title="Развернуть", control_type="Button").click()
            except pywinauto.findwindows.ElementNotFoundError:
                pass
            except Exception as e:
                print(e)

        self.is_first_graph_opened = True

    def screenshot_graph(self, name: str) -> Image:
        send_keys("{HOME}")

        graph = self.current_file_window.window(
            title=name, control_type="Window"
        ).child_window(title="GraphView", control_type="Pane")
        return graph.capture_as_image()

    def create_md_file(self, name: str):
        create_directory(self.output_dir)

        tags = create_tags(name)
        content = f"{' '.join(tags)}\n"

        file_name = name + ".md"

        create_file(os.path.join(self.output_dir, file_name), content)

    def save_screenshot(self, file_name: str, graph_name: str, image: Image):
        file = os.path.basename(file_name)
        save_path = os.path.join(f"{self.output_dir}\\{file}", f"{graph_name}.png")

        f = open(save_path, "w")
        f.write("")
        f.close()

        image.save(save_path)

        text = f"\n### #{graph_name.replace(' ', '_')}\n![[./{file_name}/{graph_name}.png]]\n"
        add_content_to_file(os.path.join(self.output_dir, f"{file_name}.md"), text)
