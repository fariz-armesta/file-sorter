import os
import shutil
from pathlib import Path
import uuid
import datetime
from pprint import pprint

from history_manager import HistoryManager

class FileSorter:
    """Sort files in a folder into subfolders based on their extensions."""
    
    def __init__(self, folder_path: str, mode: str):
        self.history = HistoryManager()
        self.folder_path = Path(folder_path)
        self.mode = mode
        self.file_dict = {}
        self.sort_by_date()
        
        if not self.folder_path.exists():
            raise FileNotFoundError(
                f"Folder does not exists: {self.folder_path}"
            )
        
        if not self.folder_path.is_dir():
            raise NotADirectoryError(
                f"Path is not a folder: {self.folder_path}"
            )
        
        if not os.access(self.folder_path, os.R_OK | os.W_OK):
            raise PermissionError(
                f"No read/write permission for folder: {self.folder_path}"
            )
        if folder_path == "":
            raise ValueError("Folder path cannot be empty.")
        
    def sort_by_date(self):
        items = self.folder_path.iterdir()
        for item in items:
            if item.is_dir():
                continue
            
            if not item.exists():
                continue
            
            if item.is_file():
                created_timestamp = item.stat().st_ctime
                created_date = datetime.datetime.fromtimestamp(created_timestamp)
                created_date = created_date.strftime("%Y-%m-%d")
                if created_date not in self.file_dict:
                    self.file_dict[created_date] = []
                
                self.file_dict[created_date].append(item.name)
        
        
    def sort(self):
        """Sort files in the folder and categorize them by extension."""
        items = self.folder_path.iterdir()
                
        for item in items:
            if item.is_dir():
                continue
            
            if not item.exists():
                continue
            
            if not item.suffix:
                continue
            
            ext_res = item.suffix[1:]
            name_res = item.stem
            
            if not ext_res:
                continue
            
            if ext_res not in self.file_dict:
                self.file_dict[ext_res] = []
            
            self.file_dict[ext_res].append(name_res)
            
    def make_folder(self):
        """Create subfolders for each file extension."""
        for ext in self.file_dict:
            folder = self.folder_path / ext.upper()
            try:
                folder.mkdir(exist_ok=True)
            except PermissionError as e:
                raise PermissionError(
                    f"Cannot create folder '{folder}': {e}"
                )

    def move_files(self):
        """Move files into their respective subfolders."""
        
        batch_id_per_job = str(uuid.uuid4())
        for ext, names in self.file_dict.items():
            destination_folder = self.folder_path / ext.upper()
            
            for name in names: 
                if self.mode == "Extention":
                    filename = f"{name}.{ext}"
                elif self.mode == "Date":
                    filename = f"{name}"
                source = self.folder_path / filename
                destination = destination_folder / filename
                
                if not source.exists():
                    continue
                
                try:
                    shutil.move(source, destination)
                    
                    self.history.add_record(
                        batch_id=batch_id_per_job,
                        file_name=filename, 
                        from_path=str(source),
                        to_path=str(destination)
                    )
                except PermissionError as e:
                    raise PermissionError(
                        f"Cannot move file '{source}' to "
                        f"'{destination}': {e}"
                    )
                except shutil.Error as e:
                    raise shutil.Error(f"Move failed: {e}")
    
    def run(self):
        """Execute the sorting process."""
        if self.mode == "Extention":
            self.sort()
            self.make_folder()
            self.move_files()
        elif self.mode == "Date":
            self.sort_by_date()
            self.make_folder()
            self.move_files()

