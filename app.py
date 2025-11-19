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
    QHBoxLayout,
    QTableWidgetItem,
    QTableWidget,
)
from PyQt6.QtGui import QIcon
 
from file_sorter import FileSorter
from history_manager import HistoryManager


class MainWindow(QMainWindow):
    """Main window for the File Sorter application."""
            
    def __init__(self):
        super().__init__()
        
        self.history = HistoryManager()
        
        self.setWindowTitle("File Sorter - Armesta")
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QIcon("ARMESTA2_small.png"))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        input_row = QHBoxLayout() 
        
        layout = QVBoxLayout()
        
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Folder Path")
        self.input_box.setFixedSize(250, 35)
        
        self.clear_button = QPushButton("X")
        self.clear_button.setFixedSize(30, 30)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #d9534f;
                color: white;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c9302c;
            }
        """)
        self.clear_button.clicked.connect(self.input_box.clear)
        
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
        
        
        button_row = QHBoxLayout()
        
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
                background-color: #4c6daf;
                color: white;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6f98e8;
            }
            QPushButton:pressed {
                background-color: #5a8df2;
            }
        """)
        
        self.table = QTableWidget()
        
        input_row.addWidget(self.input_box)
        input_row.addWidget(self.clear_button)
        layout.addLayout(input_row)
        
        button_row.addWidget(button)
        button_row.addWidget(self.button_folder)
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(button_row)        
        layout.addWidget(self.label)
        
        layout.addWidget(self.label_folder)
        layout.addWidget(self.table)
        
        history_button = QPushButton("Show History")
        
        history_button.setStyleSheet("""
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
        
        history_button.clicked.connect(self.show_history)
        layout.addWidget(history_button)
        
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
            self.file_sorter = FileSorter(path)    
            self.file_sorter.run()
        
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
            
    def show_history(self):
        """"""
        
        data = self.history.get_history()
        
        self.table.setRowCount(len(data))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Batch ID", "File Name", "From", "To", "Moved At"])
        
        for row_index, row in enumerate(data):
            self.table.setItem(row_index, 0, QTableWidgetItem(str(row["id"])))
            self.table.setItem(row_index, 1, QTableWidgetItem(row["batch_id"]))
            self.table.setItem(row_index, 2, QTableWidgetItem(row["file_name"]))
            self.table.setItem(row_index, 3, QTableWidgetItem(row["from_path"]))
            self.table.setItem(row_index, 4, QTableWidgetItem(row["to_path"]))
            self.table.setItem(row_index, 5, QTableWidgetItem(row["moved_at"]))
            
        
        