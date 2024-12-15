import os
import time
from typing import List

import cst.interface as cst_interface
import cst.results as cst_results
import pywinauto

from src import settings
from src.files import get_cst_files_in_directory, create_directory, transliterate_filename
import shutil


class CST:
    def __init__(self):
        self.input_dir = settings.input_directory_path
        self.output_dir = settings.output_directory_path
        self.is_first_run = True
        self.app_window: pywinauto.WindowSpecification = None
        self.design_envrionment = cst_interface.DesignEnvironment()

    def start_processing(self):
        time.sleep(5)

        files = get_cst_files_in_directory(self.input_dir)

        create_directory(f'{self.input_dir}\\temp')

        self.process_files(files)

    def process_files(self, files: List[str]):
        for file in files:
            processed_file = f'{self.input_dir}\\temp\\{transliterate_filename(os.path.basename(file))}'
            shutil.copy(file, processed_file)

            print(processed_file)
            project = self.design_envrionment.open_project(processed_file)
            project.modeler.run_solver()

            try:
                self.process_file(file, processed_file)
            except Exception as e:
                print(e)
                print(f"Error processing {file}")
            project.close()

            time.sleep(30)

    def process_file(self, file_name: str, processed_file_name: str):
        if self.is_first_run:
            self.app_window = pywinauto.Application(backend="uia").connect(
                title_re=f".*{file_name}.*"
            )
            self.is_first_run = False

        items = cst_results.ProjectFile(processed_file_name, allow_interactive=True).get_3d().get_tree_items()
        results = self.fitler_results(items)
        print(results)

        self.app_window.print_control_identifiers()

        time.sleep(30)

    def fitler_results(self, items: List[str]) -> List[str]:
        results = []
        for item in items:
            if '1D Results\\S-Parameters\\S' in item:
                results.append(item)

        return results