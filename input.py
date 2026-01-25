from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt6.QtCore import Qt

class InputDialog(QDialog):
	def __init__(self, title="Input", label_text="Enter value:", parent=None):
		super().__init__(parent)
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
		self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
		self.result_value = None
		
		layout = QVBoxLayout(self)
		layout.setContentsMargins(0, 0, 0, 0)
		
		self.container = QWidget()
		self.container.setObjectName("MainContainer")
		self.container.setFixedWidth(350)
		
		container_layout = QVBoxLayout(self.container)
		container_layout.setContentsMargins(20, 20, 20, 20)
		
		title_lbl = QLabel(title.upper())
		title_lbl.setObjectName("GradientLabel")
		container_layout.addWidget(title_lbl)
		
		container_layout.addWidget(QLabel(label_text))
		
		self.input_field = QLineEdit()
		self.input_field.setAlignment(Qt.AlignmentFlag.AlignCenter) # Как в unlock
		self.input_field.setFixedHeight(40)
		container_layout.addWidget(self.input_field)
		
		btn_layout = QHBoxLayout()
		ok_btn = QPushButton("ADD")
		ok_btn.clicked.connect(self.handle_ok)
		
		cancel_btn = QPushButton("CANCEL")
		cancel_btn.setObjectName("SecondaryBtn")
		cancel_btn.clicked.connect(self.reject)
		
		btn_layout.addWidget(ok_btn)
		btn_layout.addWidget(cancel_btn)
		container_layout.addLayout(btn_layout)
		
		layout.addWidget(self.container)

	def handle_ok(self):
		self.result_value = self.input_field.text().strip()
		self.accept()