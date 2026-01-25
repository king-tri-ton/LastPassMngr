from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QWidget)
from PyQt6.QtCore import Qt

class EditorDialog(QDialog):
    def __init__(self, parent=None, site="", login="", password="", title="Edit Entry"):
        super().__init__(parent)
        self.setFixedSize(280, 370)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.result_data = None
        self.init_ui(site, login, password, title)

    def init_ui(self, site, login, password, title):
        # Главный контейнер (как в основном окне)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.container = QWidget()
        self.container.setObjectName("MainContainer") # Подхватит стиль из theme.py
        container_layout = QVBoxLayout(self.container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)

        # Заголовок
        title_label = QLabel(title)
        title_label.setObjectName("GradientLabel")
        container_layout.addWidget(title_label)

        # Поля ввода
        self.site_input = QLineEdit(site)
        self.site_input.setPlaceholderText("Site (e.g. google.com)")
        
        self.login_input = QLineEdit(login)
        self.login_input.setPlaceholderText("Login / Email")
        
        self.pass_input = QLineEdit(password)
        self.pass_input.setPlaceholderText("Password")
        # self.pass_input.setEchoMode(QLineEdit.EchoMode.Password) # Если хочешь скрыть

        container_layout.addWidget(QLabel("Site:"))
        container_layout.addWidget(self.site_input)
        container_layout.addWidget(QLabel("Login:"))
        container_layout.addWidget(self.login_input)
        container_layout.addWidget(QLabel("Password:"))
        container_layout.addWidget(self.pass_input)

        # Кнопки
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("SAVE")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self.accept_data)
        
        cancel_btn = QPushButton("CANCEL")
        cancel_btn.setObjectName("CloseBtn") # Красный стиль
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        container_layout.addLayout(btn_layout)

        layout.addWidget(self.container)

    def accept_data(self):
        self.result_data = {
            'site': self.site_input.text().strip(),
            'login': self.login_input.text().strip(),
            'password': self.pass_input.text().strip()
        }
        self.accept()

