from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QApplication, QMainWindow, QPushButton
from file_sorter import *
import file_sorter

class MainWindow(QMainWindow):        
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("File Sorter")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Folder Path")
        
        self.label = QLabel("")
        
        button = QPushButton("Show Text")
        
        button.clicked.connect(self.show_text)
        
        layout.addWidget(self.input_box)
        layout.addWidget(button)
        layout.addWidget(self.label)
        central_widget.setLayout(layout)
        
    def show_text(self):
        text = self.input_box.text()
        file_sorter.folder_path = text
        sort()
        make_folder()
        move_files()
        self.label.setText(f"Folder {text} is Sorted")
        