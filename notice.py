from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt6.QtCore import Qt

class NoticeDialog(QDialog):
	def __init__(self, message, title="Notice", confirm_mode=False, parent=None):
		super().__init__(parent)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

		self.confirm_mode = confirm_mode
		self.init_ui(message, title)

	def init_ui(self, message, title):
		layout = QVBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		self.container = QWidget()
		self.container.setObjectName("MainContainer")
		self.container.setFixedWidth(350)

		container_layout = QVBoxLayout(self.container)
		container_layout.setContentsMargins(20, 20, 20, 20)
		container_layout.setSpacing(20)

		title_label = QLabel(title.upper())
		title_label.setObjectName("GradientLabel")
		title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		container_layout.addWidget(title_label)

		msg_label = QLabel(message)
		msg_label.setWordWrap(True)
		msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		msg_label.setStyleSheet("font-size: 13px; color: #E0E0E0")
		container_layout.addWidget(msg_label)

		btn_layout = QHBoxLayout()

		if self.confirm_mode:
			self.yes_btn = QPushButton("YES")
			self.yes_btn.setCursor(Qt.CursorShape.PointingHandCursor)
			self.yes_btn.clicked.connect(self.accept)

			self.no_btn = QPushButton("NO")
			self.no_btn.setObjectName("SecondaryBtn")
			self.no_btn.setCursor(Qt.CursorShape.PointingHandCursor)
			self.no_btn.clicked.connect(self.reject)

			btn_layout.addWidget(self.yes_btn)
			btn_layout.addWidget(self.no_btn)
		else:
			self.ok_btn = QPushButton("OK")
			self.ok_btn.setCursor(Qt.CursorShape.PointingHandCursor)
			self.ok_btn.clicked.connect(self.accept)
			btn_layout.addWidget(self.ok_btn)

		container_layout.addLayout(btn_layout)
		layout.addWidget(self.container)
