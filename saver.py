# Save password dialog (SavePasswordDialog class)

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
							 QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QScreen, QIcon

class SavePasswordDialog(QDialog):
	def __init__(self, password, storage, parent=None):
		super().__init__(parent)
		self.password = password
		self.storage = storage
		self.init_ui()
		self.set_window_icon()
		self.position_bottom_right()

	def init_ui(self):
		self.setWindowTitle("Save Password")
		self.setFixedSize(400, 150)

		layout = QVBoxLayout()

		# Сайт
		site_layout = QHBoxLayout()
		site_layout.addWidget(QLabel("Site:"))
		self.site_input = QLineEdit()
		site_layout.addWidget(self.site_input)
		layout.addLayout(site_layout)

		# Логин
		login_layout = QHBoxLayout()
		login_layout.addWidget(QLabel("Login:"))
		self.login_input = QLineEdit()
		login_layout.addWidget(self.login_input)
		layout.addLayout(login_layout)

		# Категория
		category_layout = QHBoxLayout()
		category_layout.addWidget(QLabel("Category:"))
		self.category_combo = QComboBox()

		# Загружаем категории
		categories = self.storage.get_categories()
		self.category_combo.addItems(categories)

		# General по умолчанию
		if "General" in categories:
			self.category_combo.setCurrentText("General")

		category_layout.addWidget(self.category_combo)
		layout.addLayout(category_layout)

		# Пароль
		password_layout = QHBoxLayout()
		password_layout.addWidget(QLabel("Password:"))
		self.password_input = QLineEdit()
		self.password_input.setText(self.password)
		self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
		self.password_input.setReadOnly(True)
		password_layout.addWidget(self.password_input)

		# Кнопка показать пароль
		self.show_password_btn = QPushButton("Show")
		self.show_password_btn.setFixedWidth(60)
		self.show_password_btn.clicked.connect(self.toggle_password_visibility)
		password_layout.addWidget(self.show_password_btn)

		layout.addLayout(password_layout)

		# Кнопки
		button_layout = QHBoxLayout()
		save_btn = QPushButton("Save")
		save_btn.clicked.connect(self.save_password)
		cancel_btn = QPushButton("Cancel")
		cancel_btn.clicked.connect(self.close)
		button_layout.addWidget(save_btn)
		button_layout.addWidget(cancel_btn)
		layout.addLayout(button_layout)

		self.setLayout(layout)
		self.site_input.setFocus()

		# Автоматическое закрытие через 30 секунд
		# QTimer.singleShot(30000, self.close)

	def set_window_icon(self):
		"""Загружает иконку, как в app.py"""
		if getattr(__import__("sys"), "frozen", False):
			base_path = __import__("sys")._MEIPASS
		else:
			base_path = os.path.dirname(os.path.abspath(__file__))

		icon_path = os.path.join(base_path, "Logo.ico")
		if os.path.exists(icon_path):
			self.setWindowIcon(QIcon(icon_path))
		else:
			self.setWindowIcon(QIcon())

	def position_bottom_right(self):
		screen = QScreen.availableGeometry(self.screen())
		x = screen.width() - self.width() - 20
		y = screen.height() - self.height() - 60
		self.move(x, y)

	def save_password(self):
		site = self.site_input.text().strip()
		login = self.login_input.text().strip()
		category = self.category_combo.currentText()

		if not site or not login:
			QMessageBox.warning(self, "Warning", "Fill all fields")
			return

		try:
			self.storage.save_password(site, login, self.password, category)
			QMessageBox.information(self, "Success", "Password saved")
			self.close()
		except Exception as e:
			QMessageBox.critical(self, "Error", str(e))

	def closeEvent(self, event):
		event.accept()

	def toggle_password_visibility(self):
		if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
			self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
			self.show_password_btn.setText("Hide")
		else:
			self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
			self.show_password_btn.setText("Show")
