# Main password manager window (PasswordManagerWindow class)

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
							 QTableWidget, QTableWidgetItem, QPushButton, 
							 QLineEdit, QLabel, QHeaderView,
							 QListWidget, QMenu)
from PyQt6.QtCore import Qt, QPoint, QSettings, QTimer
import pyperclip

from utils import DraggableMixin
from editor import EditorDialog
from notice import NoticeDialog
from input import InputDialog

class PasswordManagerWindow(DraggableMixin, QMainWindow):
	def __init__(self, storage, icon=None):
		super().__init__()
		self.storage = storage
		if icon:
			self.setWindowIcon(icon)
		self.init_ui()

	def init_ui(self):
		self._drag_pos = QPoint()
		self.setWindowTitle("Simple Password Manager by King Triton")
		
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

		self.setMinimumSize(800, 333)
		self.settings = QSettings('TritonCorp', 'SimPassMngr')
		geometry = self.settings.value('geometry')
		if geometry:
			self.restoreGeometry(geometry)
		else:
			self.resize(800, 333)

		bg_widget = QWidget()
		self.setCentralWidget(bg_widget)
		bg_layout = QVBoxLayout(bg_widget)
		bg_layout.setContentsMargins(0, 0, 0, 0)

		self.main_container = QWidget()
		self.main_container.setObjectName('MainContainer')
		self.main_container.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
		bg_layout.addWidget(self.main_container)

		main_layout = QHBoxLayout(self.main_container)
		main_layout.setContentsMargins(15, 15, 15, 15)

		# === ЛЕВАЯ ПАНЕЛЬ - Категории ===
		left_panel = QVBoxLayout()

		left_panel.addWidget(QLabel("Categories:"))

		# Список категорий
		self.categories_list = QListWidget()
		self.categories_list.currentItemChanged.connect(self.on_category_changed)
		left_panel.addWidget(self.categories_list)

		# Кнопки управления категориями
		category_buttons = QHBoxLayout()
		add_category_btn = QPushButton("Add")
		add_category_btn.clicked.connect(self.add_category)

		delete_category_btn = QPushButton("Delete")
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

		# Кнопка "Закрыть"
		exit_btn = QPushButton('CLOSE')
		exit_btn.setObjectName('CloseBtn')
		exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
		exit_btn.clicked.connect(self.close)
		search_layout.addWidget(exit_btn)

		right_panel.addLayout(search_layout)

		# Таблица
		self.table = QTableWidget()
		self.table.setColumnCount(4)
		self.table.setHorizontalHeaderLabels(['Site', 'Login / Email', 'Password', 'Actions'])

		self.table.horizontalHeader().setStretchLastSection(True)

		self.table.verticalHeader().setDefaultSectionSize(45)

		header = self.table.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
		header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
		header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
		header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
		self.table.setColumnWidth(3, 240)

		self.table.setTextElideMode(Qt.TextElideMode.ElideNone)
		header.setStretchLastSection(False)

		self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
		self.table.customContextMenuRequested.connect(self.show_context_menu)

		self.table.setTextElideMode(Qt.TextElideMode.ElideRight)
		self.table.setWordWrap(False)

		self.table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
		self.table.verticalHeader().setFixedWidth(40)

		right_panel.addWidget(self.table)

		# Добавляем панели в главный layout
		main_layout.addLayout(left_panel, 1)   # 1 часть ширины
		main_layout.addLayout(right_panel, 3)  # 3 части ширины

		self.load_categories()
		self.load_passwords()

		# --- СТАТУС-БАР (StatusBar) ---
		self.status_layout = QHBoxLayout()
		
		# Левая часть - Сообщения
		self.status_message = QLabel("")
		self.status_message.setObjectName("StatusMsg")
		
		# Правая часть - Брендинг
		self.branding_label = QLabel("LastPassMngr by King Triton v3.0.0")
		self.branding_label.setObjectName("BrandingLabel")
		
		self.status_layout.addWidget(self.status_message)
		self.status_layout.addStretch()
		self.status_layout.addWidget(self.branding_label)
		
		# Добавляем статус-бар в правую панель под таблицу
		right_panel.addLayout(self.status_layout)

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

		item_site = QTableWidgetItem(site)
		item_site.setFlags(item_site.flags() ^ Qt.ItemFlag.ItemIsEditable) # Только чтение
		item_site.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		item_login = QTableWidgetItem(login)
		item_login.setFlags(item_login.flags() ^ Qt.ItemFlag.ItemIsEditable)
		item_login.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		password_item = QTableWidgetItem('••••••••••••')
		password_item.setData(Qt.ItemDataRole.UserRole, password)
		password_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

		self.table.setItem(row, 0, item_site)
		self.table.setItem(row, 1, item_login)
		self.table.setItem(row, 2, password_item)

		# Кнопки
		actions_widget = QWidget()
		actions_layout = QHBoxLayout(actions_widget)
		actions_layout.setContentsMargins(5, 4, 5, 4)
		actions_layout.setSpacing(8)

		show_btn = QPushButton("Show")
		show_btn.setObjectName("ShowBtn")
		show_btn.setCursor(Qt.CursorShape.PointingHandCursor)
		show_btn.clicked.connect(lambda: self.toggle_password(row))

		copy_btn = QPushButton("Copy")
		copy_btn.setObjectName("CopyBtn")
		copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
		copy_btn.clicked.connect(lambda: self.copy_password(row))

		delete_btn = QPushButton("Delete")
		delete_btn.setObjectName("DeleteBtn") # Красная
		delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
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
		
		# Пишем в наш кастомный лейбл
		self.status_message.setText("Copied to clipboard!")
		
		# Очистка сообщения через 3 секунды
		QTimer.singleShot(3000, lambda: self.status_message.setText(""))

	def delete_password(self, row):
		site = self.table.item(row, 0).text()
		login = self.table.item(row, 1).text()

		# Получаем текущую категорию
		current_item = self.categories_list.currentItem()
		if not current_item:
			return

		category = current_item.text()

		dialog = NoticeDialog(
				message=f"Are you sure you want to delete password for {site}?",
				title="Confirm Delete",
				confirm_mode=True,
				parent=self
			)

		if dialog.exec():
			self.storage.delete_password(site, login, category)
			self.load_passwords()
			self.status_message.setText("Entry deleted.")
			QTimer.singleShot(3000, lambda: self.status_message.setText(""))

	def filter_passwords(self, text):
		for row in range(self.table.rowCount()):
			site = self.table.item(row, 0).text()
			login = self.table.item(row, 1).text()

			if text.lower() in site.lower() or text.lower() in login.lower():
				self.table.setRowHidden(row, False)
			else:
				self.table.setRowHidden(row, True)

	def closeEvent(self, event):
		self.settings.setValue('geometry', self.saveGeometry())
		self.hide()
		event.ignore()

	def load_categories(self):
		"""Загружает список категорий с General наверху"""
		self.categories_list.clear()
		passwords = self.storage.get_passwords()
		
		# Получаем все названия категорий
		all_categories = list(passwords.keys())
		
		# Если категорий вообще нет — создаем дефолтный список
		if not all_categories:
			all_categories = ["General"]
		
		# Сортируем: убираем General, сортируем остальное по алфавиту
		other_categories = sorted([c for c in all_categories if c != "General"])
		
		# Собираем итоговый список: General всегда первый
		final_list = ["General"] + other_categories

		for category in final_list:
			self.categories_list.addItem(category)

		# Выбираем первую (General) по умолчанию
		self.categories_list.setCurrentRow(0)

	def on_category_changed(self, current, previous):
		"""Обработчик смены категории"""
		if current:
			self.load_passwords()

	def add_category(self):
		dialog = InputDialog(title="New Category", label_text="Category name:", parent=self)
		
		if dialog.exec():
			category_name = dialog.result_value

			if category_name:
				for i in range(self.categories_list.count()):
					if self.categories_list.item(i).text().lower() == category_name.lower():
						warn = NoticeDialog(
							message=f"Category '{category_name}' already exists!",
							title="Warning",
							confirm_mode=False,
							parent=self
						)
						warn.exec()
						return

				self.storage.add_category(category_name)
				self.load_categories()

				for i in range(self.categories_list.count()):
					if self.categories_list.item(i).text() == category_name:
						self.categories_list.setCurrentRow(i)
						break

	def delete_category(self):
		"""Удаляет категорию через кастомный NoticeDialog"""
		current_item = self.categories_list.currentItem()

		if not current_item:
			return

		category = current_item.text()

		# 1. Защита General
		if category == "General":
			warn = NoticeDialog(
				message="Cannot delete 'General' category.\nThis is your default vault.",
				title="Access Denied",
				confirm_mode=False,
				parent=self
			)
			warn.exec()
			return

		# 2. Подтверждение удаления
		dialog = NoticeDialog(
			message=f'Delete category "{category}" and all passwords in it? This action cannot be undone.',
			title="Delete Category",
			confirm_mode=True,
			parent=self
		)

		if dialog.exec():
			self.storage.delete_category(category)
			self.load_categories()
			self.status_message.setText(f"Category '{category}' removed.")
			QTimer.singleShot(3000, lambda: self.status_message.setText(""))

	def show_context_menu(self, pos):
		index = self.table.indexAt(pos)
		if not index.isValid():
			return

		row = index.row()
		site = self.table.item(row, 0).text()
		login = self.table.item(row, 1).text()
		# Получаем текущую категорию из UI (списка слева)
		current_category = self.categories_list.currentItem().text()

		menu = QMenu(self)
		
		# Основные действия
		edit_action = menu.addAction("Edit Entry")
		copy_login_action = menu.addAction("Copy Login")
		
		# --- ВЛОЖЕННОЕ МЕНЮ "Move to" ---
		move_menu = menu.addMenu("Move to")
		
		# Получаем список всех категорий из хранилища
		categories = self.storage.get_categories() # Предположим, такой метод есть
		
		for category in categories:
			if category != current_category:  # Не показываем ту, где мы уже находимся
				action = move_menu.addAction(category)
				# Используем замыкание для передачи категории в обработчик
				action.triggered.connect(lambda checked, c=category: self.move_entry(row, c))
		
		menu.addSeparator()
		delete_action = menu.addAction("Delete")

		# Выполняем меню
		action = menu.exec(self.table.viewport().mapToGlobal(pos))

		if action == edit_action:
			self.edit_password_entry(row)
		elif action == copy_login_action:
			pyperclip.copy(login)
			self.status_message.setText("Login copied!")
			QTimer.singleShot(3000, lambda: self.status_message.setText(""))
		elif action == delete_action:
			self.delete_password(row)

	def move_entry(self, row, new_category):
		site = self.table.item(row, 0).text()
		login = self.table.item(row, 1).text()
		old_category = self.categories_list.currentItem().text()
		
		# Вызываем метод перемещения в твоем storage
		# Тебе нужно будет реализовать этот метод в классе Storage
		if self.storage.move_password(site, login, old_category, new_category):
			self.load_passwords() # Перезагружаем таблицу
			self.status_message.setText(f"Moved to {new_category}")
			QTimer.singleShot(3000, lambda: self.status_message.setText(""))
		else:
			print("Error: Failed to move entry")

	def edit_password_entry(self, row):
		# Достаем старые данные
		old_site = self.table.item(row, 0).text()
		old_login = self.table.item(row, 1).text()
		old_password = self.table.item(row, 2).data(Qt.ItemDataRole.UserRole)
		current_category = self.categories_list.currentItem().text()

		# Открываем диалог
		dialog = EditorDialog(self, old_site, old_login, old_password)
		if dialog.exec():
			new_data = dialog.result_data
			
			# Сначала удаляем старую запись, потом добавляем новую
			# Это самый простой способ "редактирования" в текущей архитектуре storage
			self.storage.delete_password(old_site, old_login, current_category)
			self.storage.save_password(
				new_data['site'], 
				new_data['login'], 
				new_data['password'], 
				current_category
			)
			
			self.load_passwords()
			self.status_message.setText("Entry updated successfully!")
			QTimer.singleShot(3000, lambda: self.status_message.setText(""))

