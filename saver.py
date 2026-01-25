# Save password dialog (SavePasswordDialog class)

import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
							 QLabel, QLineEdit, QPushButton, QComboBox, QWidget)
from PyQt6.QtCore import Qt
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
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

		# Используем тот же контейнер для золотой рамки
		self.main_container = QWidget()
		self.main_container.setObjectName("MainContainer")

		layout = QVBoxLayout(self.main_container)
		layout.setContentsMargins(25, 25, 25, 25)
		layout.setSpacing(12)

		# ЗАГОЛОВОК
		title = QLabel("SAVE PASSWORD")
		title.setObjectName("GradientLabel")
		title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		layout.addWidget(title)

		# Errors
		self.error_label = QLabel("")
		self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.error_label.setStyleSheet("color: #E63946; font-size: 11px;")
		layout.addWidget(self.error_label)

		# ПОЛЯ (Сайт, Логин, Категория)
		self.site_input = QLineEdit()
		self.site_input.setPlaceholderText("Site (e.g. google.com)")
		self.site_input.setFixedHeight(35)
		layout.addWidget(self.site_input)

		self.login_input = QLineEdit()
		self.login_input.setPlaceholderText("Login / Email")
		self.login_input.setFixedHeight(35)
		layout.addWidget(self.login_input)

		# Категория (выпадающий список)
		self.category_combo = QComboBox()
		self.category_combo.setFixedHeight(35)
		self.category_combo.addItems(self.storage.get_categories())
		if "General" in self.storage.get_categories():
		    self.category_combo.setCurrentText("General")
		layout.addWidget(self.category_combo)

		# ПАРОЛЬ (Максимально простой и жесткий код)
		pass_layout = QHBoxLayout()
		pass_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
		pass_layout.setSpacing(10)
		pass_layout.setContentsMargins(0, 0, 0, 0)

		self.password_input = QLineEdit()
		self.password_input.setText(self.password)
		self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
		self.password_input.setReadOnly(True)
		self.password_input.setFixedHeight(35)
		self.password_input.setStyleSheet("color: #F2C73C; font-weight: bold;")

		self.show_pass_btn = QPushButton("Show")
		self.show_pass_btn.setObjectName("SecondaryBtn")
		self.show_pass_btn.setFixedSize(70, 35) 
		self.show_pass_btn.clicked.connect(self.toggle_password_visibility)

		pass_layout.addWidget(self.password_input)
		pass_layout.addWidget(self.show_pass_btn)

		layout.addLayout(pass_layout)

		# КНОПКИ
		btn_layout = QHBoxLayout()
		save_btn = QPushButton("SAVE")
		save_btn.setFixedHeight(35)
		save_btn.clicked.connect(self.save_password)

		cancel_btn = QPushButton("CANCEL")
		cancel_btn.setFixedHeight(35)
		cancel_btn.setObjectName("SecondaryBtn")
		cancel_btn.clicked.connect(self.close)

		btn_layout.addWidget(save_btn)
		btn_layout.addWidget(cancel_btn)
		layout.addLayout(btn_layout)

		# Финальная упаковка
		final_layout = QVBoxLayout(self)
		final_layout.setContentsMargins(0, 0, 0, 0)
		final_layout.addWidget(self.main_container)

		self.adjustSize()
		self.setFixedWidth(350)

	def set_window_icon(self):
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
			self.error_label.setText('Error: Fill all fields!')
			return

		try:
			self.storage.save_password(site, login, self.password, category)
			self.close()
		except Exception as e:
			self.error_label.setText(f"Error: {str(e)}")

	def closeEvent(self, event):
		event.accept()

	def toggle_password_visibility(self):
		if self.password_input.echoMode() == QLineEdit.EchoMode.Password:
			self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
			self.show_pass_btn.setText("Hide")
		else:
			self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
			self.show_pass_btn.setText("Show")
