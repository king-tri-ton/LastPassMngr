# Master password dialog (MasterPasswordDialog class)

import os
import sys
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
							 QLabel, QLineEdit, QPushButton, QCheckBox)
from PyQt6.QtCore import Qt


class MasterPasswordDialog(QDialog):
	def __init__(self, is_first_time=False, parent=None):
		super().__init__(parent)
		self.is_first_time = is_first_time
		self.password = None
		self.init_ui()

	def init_ui(self):
		if self.is_first_time:
			self.setWindowTitle("Create Master Password")
		else:
			self.setWindowTitle("Enter Master Password")

		self.setFixedSize(400, 180)
		self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

		if getattr(sys, 'frozen', False):
			base_path = sys._MEIPASS
		else:
			base_path = os.path.dirname(os.path.abspath(__file__))

		icon_path = os.path.join(base_path, "Logo.ico")
		if os.path.exists(icon_path):
			from PyQt6.QtGui import QIcon
			self.setWindowIcon(QIcon(icon_path))

		layout = QVBoxLayout()

		# Заголовок
		if self.is_first_time:
			title = QLabel("Create your master password\nThis password will protect all your stored passwords")
		else:
			title = QLabel("Enter your master password to unlock")

		title.setWordWrap(True)
		layout.addWidget(title)

		# Поле пароля
		password_layout = QHBoxLayout()
		password_layout.addWidget(QLabel("Master Password:"))
		self.password_input = QLineEdit()
		self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
		self.password_input.returnPressed.connect(self.accept_password)
		password_layout.addWidget(self.password_input)
		layout.addLayout(password_layout)

		# Чекбокс показать пароль
		self.show_password_checkbox = QCheckBox("Show password")
		self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
		layout.addWidget(self.show_password_checkbox)

		# Подтверждение пароля (только при создании)
		if self.is_first_time:
			confirm_layout = QHBoxLayout()
			confirm_layout.addWidget(QLabel("Confirm Password:"))
			self.confirm_input = QLineEdit()
			self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
			self.confirm_input.returnPressed.connect(self.accept_password)
			confirm_layout.addWidget(self.confirm_input)
			layout.addLayout(confirm_layout)

		# Кнопки
		button_layout = QHBoxLayout()
		ok_btn = QPushButton("OK")
		ok_btn.clicked.connect(self.accept_password)
		cancel_btn = QPushButton("Cancel")
		cancel_btn.clicked.connect(self.reject)
		button_layout.addWidget(ok_btn)
		button_layout.addWidget(cancel_btn)
		layout.addLayout(button_layout)

		self.setLayout(layout)
		self.password_input.setFocus()
	
	def toggle_password_visibility(self, state):
		if state == Qt.CheckState.Checked.value:
			self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
			if self.is_first_time:
				self.confirm_input.setEchoMode(QLineEdit.EchoMode.Normal)
		else:
			self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
			if self.is_first_time:
				self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
	
	def accept_password(self):
		password = self.password_input.text()

		if not password:
			return

		if self.is_first_time:
			confirm = self.confirm_input.text()
			if password != confirm:
				self.password_input.clear()
				self.confirm_input.clear()
				self.password_input.setFocus()
				self.setWindowTitle("Passwords don't match - try again")
				return

		self.password = password
		self.accept()
	
	def get_password(self):
		return self.password