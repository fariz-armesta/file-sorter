from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMessageBox, 
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QLineEdit,  
    QMainWindow, 
    QPushButton,
    QFileDialog,
)
from PyQt6.QtGui import QIcon
 
from file_sorter import FileSorter


class MainWindow(QMainWindow):
    """Main window for the File Sorter application."""
            
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("File Sorter - Armesta")
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QIcon("ARMESTA2_small.png"))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Folder Path")
        self.input_box.setFixedSize(250, 35)
        self.input_box.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ccc;
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #4CAF50
            }                                     
                                                        
        """)
        
        self.label = QLabel("")
        
        button = QPushButton("Clean Folder")
        button.setFixedSize(150, 40)
        
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        
        button.clicked.connect(self.show_text)
        
        self.label_folder = QLabel("")
        self.button_folder = QPushButton("Select Folder")
        self.button_folder.clicked.connect(self.select_folder)
        
        self.button_folder.setFixedSize(150, 40)
        
        self.button_folder.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        
        layout.addWidget(self.input_box, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        layout.addWidget(self.button_folder, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_folder)
        
        central_widget.setLayout(layout)
        
    def show_error(self, message):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.exec()
        self.input_box.clear()
        
            
    def show_text(self):
        path = self.input_box.text()
        
        try:
            file_sorter = FileSorter(path)    
            file_sorter.run()
        
            msg = QMessageBox()
            msg.setWindowTitle("Sorting Complete")
            msg.setText(f"folder'{path}' is sorted successfully")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.exec()
            self.input_box.clear()
            
        except FileNotFoundError as e:
            self.show_error(str(e))
            self.input_box.clear()
            
        except NotADirectoryError as e:
            self.show_error(str(e))
            self.input_box.clear()
            
        except PermissionError as e:
            self.show_error(str(e))
            self.input_box.clear()
            
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        
        if folder:
            self.input_box.setText(folder)
            
        
        