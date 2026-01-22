# Main password manager window (PasswordManagerWindow class)

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
		self.setGeometry(100, 100, 700, 400)

		central_widget = QWidget()
		self.setCentralWidget(central_widget)

		# Главный layout с разделением на левую панель и правую
		main_layout = QHBoxLayout()

		# === ЛЕВАЯ ПАНЕЛЬ - Категории ===
		left_panel = QVBoxLayout()

		left_panel.addWidget(QLabel("Categories:"))

		# Список категорий
		from PyQt6.QtWidgets import QListWidget
		self.categories_list = QListWidget()
		self.categories_list.currentItemChanged.connect(self.on_category_changed)
		left_panel.addWidget(self.categories_list)

		# Кнопки управления категориями
		category_buttons = QHBoxLayout()
		add_category_btn = QPushButton("+")
		add_category_btn.setFixedWidth(40)
		add_category_btn.clicked.connect(self.add_category)

		delete_category_btn = QPushButton("-")
		delete_category_btn.setFixedWidth(40)
		delete_category_btn.clicked.connect(self.delete_category)

		category_buttons.addWidget(add_category_btn)
		category_buttons.addWidget(delete_category_btn)
		category_buttons.addStretch()

		left_panel.addLayout(category_buttons)

		# === ПРАВАЯ ПАНЕЛЬ - Пароли ===
		right_panel = QVBoxLayout()

		# Поиск
		search_layout = QHBoxLayout()
		search_layout.addWidget(QLabel("Search:"))
		self.search_input = QLineEdit()
		self.search_input.textChanged.connect(self.filter_passwords)
		search_layout.addWidget(self.search_input)

		refresh_btn = QPushButton("Refresh")
		refresh_btn.clicked.connect(self.load_passwords)
		search_layout.addWidget(refresh_btn)

		right_panel.addLayout(search_layout)

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

		right_panel.addWidget(self.table)

		# Добавляем панели в главный layout
		main_layout.addLayout(left_panel, 1)   # 1 часть ширины
		main_layout.addLayout(right_panel, 3)  # 3 части ширины

		central_widget.setLayout(main_layout)

		self.load_categories()
		self.load_passwords()

	def load_passwords(self):
		self.table.setRowCount(0)

		# Получаем текущую выбранную категорию
		current_item = self.categories_list.currentItem()
		if not current_item:
			return

		current_category = current_item.text()

		passwords = self.storage.get_passwords()

		# Проверяем формат данных (старый или новый)
		for key, value in passwords.items():
			if isinstance(value, list):
				# Старый формат: {site: [entries]}
				if current_category == "General":
					for entry in value:
						self.add_table_row(key, entry['login'], entry['password'], "General")
			elif isinstance(value, dict):
				# Новый формат: {category: {site: [entries]}}
				if key == current_category:
					for site, entries in value.items():
						for entry in entries:
							self.add_table_row(site, entry['login'], entry['password'], key)

	def add_table_row(self, site, login, password, category="General"):
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

		# Получаем текущую категорию
		current_item = self.categories_list.currentItem()
		if not current_item:
			return

		category = current_item.text()

		reply = QMessageBox.question(self, 'Delete', 
									 f'Delete password for {site}?',
									 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

		if reply == QMessageBox.StandardButton.Yes:
			self.storage.delete_password(site, login, category)
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

	def load_categories(self):
		"""Загружает список категорий"""
		self.categories_list.clear()
		passwords = self.storage.get_passwords()

		for category in passwords.keys():
			self.categories_list.addItem(category)

		# Если категорий нет, добавляем General
		if self.categories_list.count() == 0:
			self.categories_list.addItem("General")

		# Выбираем первую категорию
		if self.categories_list.count() > 0:
			self.categories_list.setCurrentRow(0)

	def on_category_changed(self, current, previous):
		"""Обработчик смены категории"""
		if current:
			self.load_passwords()

	def add_category(self):
		"""Добавляет новую категорию"""
		from PyQt6.QtWidgets import QInputDialog

		category_name, ok = QInputDialog.getText(self, "New Category", "Category name:")

		if ok and category_name.strip():
			category_name = category_name.strip()

			# Проверяем, не существует ли уже
			for i in range(self.categories_list.count()):
				if self.categories_list.item(i).text() == category_name:
					QMessageBox.warning(self, "Warning", "Category already exists")
					return

			# Добавляем категорию
			self.storage.add_category(category_name)
			self.load_categories()

			# Выбираем новую категорию
			for i in range(self.categories_list.count()):
				if self.categories_list.item(i).text() == category_name:
					self.categories_list.setCurrentRow(i)
					break

	def delete_category(self):
		"""Удаляет категорию"""
		current_item = self.categories_list.currentItem()

		if not current_item:
			return

		category = current_item.text()

		# Нельзя удалить General
		if category == "General":
			QMessageBox.warning(self, "Warning", "Cannot delete 'General' category")
			return

		reply = QMessageBox.question(self, 'Delete Category', 
									 f'Delete category "{category}" and all passwords in it?',
									 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

		if reply == QMessageBox.StandardButton.Yes:
			self.storage.delete_category(category)
			self.load_categories()