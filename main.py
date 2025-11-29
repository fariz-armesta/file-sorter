import sys

from PyQt6.QtWidgets import QApplication

from app import MainWindow

import ctypes

def main():
    """Main function to run the File Sorter application."""
    
    myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
    
if __name__ == "__main__":
    main()