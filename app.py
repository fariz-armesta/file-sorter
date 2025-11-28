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
        self.setup_style()
        self.window_setup()
        
        self.history = HistoryManager()
        
        self.create_home_page()
        self.setup_connection()
        
    def create_home_page(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.input_row = QHBoxLayout() 
        self.layout = QVBoxLayout()

        self.input_box = QLineEdit()

        self.button_row = QHBoxLayout()
        
        self.label = QLabel("")
        
        self.label_folder = QLabel("")
        
        self.table = QTableWidget()
        self.action_buttons()
        
        central_widget.setLayout(self.layout)    
        
    def setup_style(self):
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())
        
    def action_buttons(self):
        self.input_box.setPlaceholderText("Folder Path")
        self.input_box.setFixedSize(250, 35)
        self.input_box.setObjectName("input_box")
        
        self.clear_button = self.create_button(
            "X", "clear_button", height=30, width=30
        )
        
        self.input_row.addWidget(self.input_box)
        self.input_row.addWidget(self.clear_button)
        self.layout.addLayout(self.input_row)
        
        self.button = self.create_button(
            "Clean Folder", "clean_button"
        )
        self.button_row.addWidget(self.button)
        
        self.button_folder = self.create_button(
            "Select Folder", "folder_button"
        )
        self.button_row.addWidget(self.button_folder)
        
        self.button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(self.button_row)        
        self.layout.addWidget(self.label)
        
        self.create_table()
        
        self.history_button = self.create_button(
            "Show History", "history_button", no_size=True
        )
        
        self.layout.addWidget(self.history_button)
        
        self.delete_button = self.create_button(
            "Delete All History", "delete_button", no_size=True
        )
        
        self.layout.addWidget(self.delete_button)
        
    def create_table(self):
        self.layout.addWidget(self.label_folder)
        self.layout.addWidget(self.table)
    
    def window_setup(self):
        self.setWindowTitle("File Sorter - Armesta")
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QIcon("ARMESTA2_small.png"))
    
    def create_button(self, text, obj_name, height=40, width=150, no_size=False):
        button = QPushButton(text)
        button.setObjectName(obj_name)
        if no_size == False:
            button.setFixedSize(width, height)
            return button
        else:
            return button 
           
    def setup_connection(self):
        self.clear_button.clicked.connect(self.input_box.clear)
        self.button.clicked.connect(self.show_text)
        self.button_folder.clicked.connect(self.select_folder)
        self.history_button.clicked.connect(self.show_history)
        self.delete_button.clicked.connect(self.delete_history)
        
    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)
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
        except ValueError as e:
            self.show_error(str(e))
            
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
            
    def delete_history(self):
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete all history records?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.history.delete_all_history()
            self.table.setRowCount(0) 
            
            QMessageBox.information (
                self,
                "History Deleted",
                "All history records have been deleted.")
        