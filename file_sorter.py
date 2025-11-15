import os
import shutil
from pathlib import Path

class FileSorter:
    def __init__(self, folder_path: str):
        self.folder_path = Path(folder_path)
        self.file_dict = {}
        
        if not self.folder_path.exists():
            raise FileNotFoundError(f"Folder does not exists: {self.folder_path}")
        
        if not self.folder_path.is_dir():
            raise NotADirectoryError(f"Path is not a folder: {self.folder_path}")
        
    def sort(self):
        items = self.folder_path.iterdir()
                
        for item in items:
            if item.is_dir():
                continue
            
            ext_res = item.suffix[1:]
            name_res = item.stem
            
            if not ext_res:
                continue
            
            if ext_res not in self.file_dict:
                self.file_dict[ext_res] = []
            
            self.file_dict[ext_res].append(name_res)

    def make_folder(self):
        for ext in self.file_dict:
            folder = self.folder_path / ext
            folder.mkdir(exist_ok=True)

    def move_files(self):
        
        for ext, names in self.file_dict.items():
            destination_folder = self.folder_path / ext
            for name in names: 
                filename = f"{name}.{ext}"
                source = self.folder_path / filename
                destination = destination_folder / filename
                
                if source.exists():
                    shutil.move(source, destination)
    
    def run(self):
        self.sort()
        self.make_folder()
        self.move_files()