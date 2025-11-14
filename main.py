import sys
from file_sorter import *
from PyQt6.QtWidgets import QApplication
from app import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()