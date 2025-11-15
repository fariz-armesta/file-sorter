import sys
from file_sorter import *
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from app import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("ARMESTA2_small.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
if __name__ == "__main__":
    main()