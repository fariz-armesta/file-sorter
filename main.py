import sys
from file_sorter import *
from PyQt6.QtWidgets import QApplication
from app import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    #folder_path = input("Enter path: ")
    #sort(folder_path)
    #make_folder()
    #move_files()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()