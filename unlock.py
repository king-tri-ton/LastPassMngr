# Master password dialog (MasterPasswordDialog class)

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
							 QLabel, QLineEdit, QPushButton, QCheckBox, QWidget)
from PyQt6.QtCore import Qt

from storage import PasswordStorage


class MasterPasswordDialog(QDialog):
	def __init__(self, is_first_time=False, parent=None):
		super().__init__(parent)
		self.is_first_time = is_first_time
		self.password = None
		self.init_ui()

	def init_ui(self):
		self.setWindowTitle("LastPassMngr")
		# Убираем стандартную рамку Windows, чтобы наша золотая рамка была видна
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Нужно для скруглений/рамок

		# ГЛАВНЫЙ КОНТЕЙНЕР (нужен для отрисовки рамки через QSS)
		self.main_container = QWidget()
		self.main_container.setObjectName("MainContainer")
		
		layout = QVBoxLayout(self.main_container)
		layout.setContentsMargins(30, 30, 30, 30)
		layout.setSpacing(15)

		# 1. ЗАГОЛОВОК
		self.title_label = QLabel("MASTER KEY")
		self.title_label.setObjectName("GradientLabel")
		self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(self.title_label)

		status_text = "Create your secure vault" if self.is_first_time else "Vault is locked"
		self.subtitle = QLabel(status_text)
		self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.subtitle.setStyleSheet("color: #80868b; font-size: 11px;")
		layout.addWidget(self.subtitle)

		# 2. ПОЛЯ ВВОДА
		self.password_input = QLineEdit()
		self.password_input.setPlaceholderText("Master password...")
		self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
		self.password_input.setFixedHeight(40)
		self.password_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

		layout.addWidget(self.password_input)

		if self.is_first_time:
			self.confirm_input = QLineEdit()
			self.confirm_input.setPlaceholderText("Confirm password...")
			self.confirm_input.setEchoMode(QLineEdit.EchoMode.Password)
			self.confirm_input.setFixedHeight(40)
			self.confirm_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
			layout.addWidget(self.confirm_input)

		# 3. ЧЕКБОКС
		self.show_pass = QCheckBox("Show characters")
		self.show_pass.stateChanged.connect(self.toggle_password_visibility)
		layout.addWidget(self.show_pass)

		# 4. КНОПКИ
		btn_layout = QHBoxLayout()
		self.ok_btn = QPushButton("UNLOCK" if not self.is_first_time else "CREATE")
		self.ok_btn.setFixedHeight(35)
		self.ok_btn.clicked.connect(self.accept_password)
		
		self.exit_btn = QPushButton("EXIT")
		self.exit_btn.setFixedHeight(35)
		self.exit_btn.setObjectName("SecondaryBtn")
		self.exit_btn.clicked.connect(self.reject)

		btn_layout.addWidget(self.ok_btn)
		btn_layout.addWidget(self.exit_btn)
		layout.addLayout(btn_layout)

		# Упаковываем контейнер в основной лейаут окна
		final_layout = QVBoxLayout(self)
		final_layout.setContentsMargins(0, 0, 0, 0)
		final_layout.addWidget(self.main_container)

		# Авто-подбор размера под контент
		self.adjustSize()
		self.setFixedWidth(350) # Ширину держим ровно
	
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
			self.show_error('Error: Password cannot be empty!')
			return

		if self.is_first_time:
			confirm = self.confirm_input.text()
			if password != confirm:
				self.show_error("Error: Password don't match!")
				return
		else:
			try:
				temp_storage = PasswordStorage(password)
				if not temp_storage.verify_master_password():
					self.show_error('Error: Wrong master password!')
					return
			except Exception as e:
				self.show_error('Error: Could not verufy vault.')
				return

		self.password = password
		self.accept()

	def show_error(self, text):
		self.password_input.clear()
		if self.is_first_time:
			self.confirm_input.clear()
		self.password_input.setFocus()
		self.subtitle.setText(text)
		self.subtitle.setStyleSheet('color: #E63946; font-size: 11px;')
	
	def get_password(self):
		return self.password

	