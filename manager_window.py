from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, 
                             QLineEdit, QLabel, QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt
import pyperclip

class PasswordManagerWindow(QMainWindow):
    def __init__(self, storage, icon=None):
        super().__init__()
        self.storage = storage
        if icon:
            self.setWindowIcon(icon)
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("LastPassMngr")
        self.setGeometry(100, 100, 500, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Поиск
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_passwords)
        search_layout.addWidget(self.search_input)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_passwords)
        search_layout.addWidget(refresh_btn)
        
        layout.addLayout(search_layout)
        
        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['Site', 'Login', 'Password', 'Actions'])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 250)
        
        layout.addWidget(self.table)
        central_widget.setLayout(layout)
        
        self.load_passwords()
    
    def load_passwords(self):
        self.table.setRowCount(0)
        passwords = self.storage.get_passwords()
        
        for site, entries in passwords.items():
            for entry in entries:
                self.add_table_row(site, entry['login'], entry['password'])
    
    def add_table_row(self, site, login, password):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        self.table.setItem(row, 0, QTableWidgetItem(site))
        self.table.setItem(row, 1, QTableWidgetItem(login))
        
        password_item = QTableWidgetItem('••••••••••••')
        password_item.setData(Qt.ItemDataRole.UserRole, password)
        self.table.setItem(row, 2, password_item)
        
        # Кнопки
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 2, 5, 2)
        
        show_btn = QPushButton("Show")
        show_btn.clicked.connect(lambda: self.toggle_password(row))
        
        copy_btn = QPushButton("Copy")
        copy_btn.clicked.connect(lambda: self.copy_password(row))
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(lambda: self.delete_password(row))
        
        actions_layout.addWidget(show_btn)
        actions_layout.addWidget(copy_btn)
        actions_layout.addWidget(delete_btn)
        
        self.table.setCellWidget(row, 3, actions_widget)
    
    def toggle_password(self, row):
        password_item = self.table.item(row, 2)
        password = password_item.data(Qt.ItemDataRole.UserRole)
        
        actions_widget = self.table.cellWidget(row, 3)
        show_btn = actions_widget.layout().itemAt(0).widget()
        
        if password_item.text() == '••••••••••••':
            password_item.setText(password)
            show_btn.setText("Hide")
        else:
            password_item.setText('••••••••••••')
            show_btn.setText("Show")
    
    def copy_password(self, row):
        password_item = self.table.item(row, 2)
        password = password_item.data(Qt.ItemDataRole.UserRole)
        pyperclip.copy(password)
        self.statusBar().showMessage("Copied", 2000)
    
    def delete_password(self, row):
        site = self.table.item(row, 0).text()
        login = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(self, 'Delete', 
                                     f'Delete password for {site}?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.storage.delete_password(site, login)
            self.load_passwords()
    
    def filter_passwords(self, text):
        for row in range(self.table.rowCount()):
            site = self.table.item(row, 0).text()
            login = self.table.item(row, 1).text()
            
            if text.lower() in site.lower() or text.lower() in login.lower():
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)
    
    def closeEvent(self, event):
        self.hide()
        event.ignore()