from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QMessageBox, QWidget, QLabel, QVBoxLayout, QLineEdit, QApplication, QMainWindow, QPushButton
from PyQt6.QtGui import QIcon 
import file_sorter

class MainWindow(QMainWindow):        
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("File Sorter - Armesta")
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QIcon("Logo.jpg"))
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
        
        layout.addWidget(self.input_box, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        central_widget.setLayout(layout)
        
        
    def show_text(self):
        text = self.input_box.text()
        file_sorter.folder_path = text
        file_sorter.sort()
        file_sorter.make_folder()
        file_sorter.move_files()
        
        msg = QMessageBox()
        msg.setWindowTitle("Sorting Complete")
        msg.setText(f"folder'{text}' is sorted successfully")
        msg.setIcon(QMessageBox.Icon.Information)
        msg.exec()
        self.input_box.clear()
        
        