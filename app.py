import os
import sys
import pyperclip
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMessageBox
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QTimer, Qt, QPoint

from generator import generate_password
from storage import PasswordStorage
from saver import SavePasswordDialog
from manager import PasswordManagerWindow
from unlock import MasterPasswordDialog


class PasswordGeneratorApp:
	def __init__(self):
		self.app = QApplication(sys.argv)
		self.app.setQuitOnLastWindowClosed(False)

		master_password = self.request_master_password()
		if not master_password:
			sys.exit(0)

		try:
			self.storage = PasswordStorage(master_password)

			if not self.storage.verify_master_password():
				QMessageBox.critical(None, "Error", "Wrong master password!")
				sys.exit(1)

		except Exception as e:
			QMessageBox.critical(None, "Error", f"Failed to initialize: {str(e)}")
			sys.exit(1)

		self.manager_window = None

		if getattr(sys, 'frozen', False):
			base_path = sys._MEIPASS
		else:
			base_path = os.path.dirname(os.path.abspath(__file__))

		icon_path = os.path.join(base_path, "Logo.ico")
		if os.path.exists(icon_path):
			self.icon = QIcon(icon_path)
		else:
			self.icon = QIcon()

		self.tray = QSystemTrayIcon()
		self.tray.setIcon(self.icon)
		self.tray.setToolTip("Password Manager")

		self.create_menu()
		self.tray.show()
	
	def request_master_password(self):
		"""Запрашивает мастер-пароль при запуске"""
		storage_dir = Path.home() / "Documents" / "LastPassMngr"
		storage_file = storage_dir / "passwords.enc"

		is_first_time = not storage_file.exists()

		dialog = MasterPasswordDialog(is_first_time=is_first_time)

		if dialog.exec():
			return dialog.get_password()
		return None
	
	def create_menu(self):
		self.menu = QMenu()

		generate_action = self.menu.addAction("Generate and Copy")
		generate_action.triggered.connect(self.generate_and_copy)

		manager_action = self.menu.addAction("Manager")
		manager_action.triggered.connect(self.open_manager)

		self.menu.addSeparator()

		exit_action = self.menu.addAction("Exit")
		exit_action.triggered.connect(self.exit_program)

		self.tray.activated.connect(self.show_tray_menu)

	def show_tray_menu(self, reason):
		if reason == QSystemTrayIcon.ActivationReason.Context:
			screen = QApplication.primaryScreen().availableGeometry()
			cursor_pos = QCursor.pos()

			adjusted_pos = QPoint(cursor_pos.x(), min(cursor_pos.y(), screen.bottom() - self.menu.sizeHint().height() - 10))

			self.menu.popup(adjusted_pos)
	
	def generate_and_copy(self):
		password = generate_password(16)
		pyperclip.copy(password)

		self.tray.showMessage(
			"Password Generated",
			"Password copied to clipboard",
			QSystemTrayIcon.MessageIcon.Information,
			2000
		)

		QTimer.singleShot(100, lambda: self.show_save_dialog(password))
	
	def show_save_dialog(self, password):
		dialog = SavePasswordDialog(password, self.storage)
		dialog.exec()
	
	def open_manager(self):
		if self.manager_window is None:
			self.manager_window = PasswordManagerWindow(self.storage, self.icon)

		self.manager_window.show()
		self.manager_window.activateWindow()
		self.manager_window.load_passwords()
	
	def exit_program(self):
		QApplication.quit()
	
	def run(self):
		sys.exit(self.app.exec())


if __name__ == "__main__":
	app = PasswordGeneratorApp()
	app.run()