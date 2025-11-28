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
    QStackedWidget,
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
        self.setup_wdidgets()
        
        self.history = HistoryManager()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        input_row = QHBoxLayout() 
        layout = QVBoxLayout()
        nav_layout = QVBoxLayout()
        
        self.btn_home.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_second.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        
        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.btn_second)
        nav_layout.addStretch()
        
        self.stack = QStackedWidget()
        
        layout.addLayout(nav_layout)
        layout.addWidget(self.stack, stretch=1)
        
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Folder Path")
        self.input_box.setFixedSize(250, 35)
        self.input_box.setObjectName("input_box")
        
        self.clear_button = self.create_button(
            "X", "clear_button", height=30, width=30
        )
        self.clear_button.clicked.connect(self.input_box.clear)

        
        button_row = QHBoxLayout()
        
        self.label = QLabel("")
        
        button = self.create_button(
            "Clean Folder", "clean_button"
        )
        button.clicked.connect(self.show_text)
        
        
        self.label_folder = QLabel("")
        self.button_folder = self.create_button(
            "Select Folder", "folder_button"
        )
        self.button_folder.clicked.connect(self.select_folder)
          
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
        
        
        self.history_button = self.create_button(
            "Show History", "history_button", no_size=True
        )
        self.history_button.clicked.connect(self.show_history)
        
        
        layout.addWidget(self.history_button)
        
        self.delete_button = self.create_button(
            "Delete All History", "delete_button"
        )
        self.delete_button.clicked.connect(self.delete_history)
        
        layout.addWidget(self.delete_button)
        
        central_widget.setLayout(layout)
        
    def setup_style(self):
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())
        
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
        
    def setup_wdidgets(self):
        self.btn_home = QPushButton("Home")
        self.btn_second = QPushButton("Second Page")
        
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
        