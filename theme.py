style = """
/* --- ОСНОВНОЕ ОКНО И ФОН --- */
QWidget {
	background-color: #202124;
	color: #E8EAED;
	font-family: 'Segoe UI', sans-serif;
	font-size: 14px;
}

/* --- ТАБЛИЦЫ (QTableWidget) --- */
QTableWidget {
	background-color: #202124;
	color: #E8EAED;
	gridline-color: #2d2e31;
	border: 1px solid #3c4043;
	selection-background-color: #3c4043;
	selection-color: #F2E167;
	outline: none;
}
QHeaderView::section {
	background-color: #303134;
	color: #F2C73C;
	padding: 5px;
	border: 1px solid #3c4043;
	font-weight: bold;
}
/* Убираем точки на заголовках */
QTableCornerButton::section {
	background-color: #303134;
	border: 1px solid #3c4043;
}

/* --- СПИСКИ (QListWidget) --- */
QListWidget {
	background-color: #202124;
	border: 1px solid #3c4043;
	border-radius: 4px;
	outline: none;
}
QListWidget::item {
	padding: 8px;
	color: #E8EAED;
}
QListWidget::item:selected {
	background-color: #3c4043;
	color: #F2C73C;
	border-left: 3px solid #F2C73C;
}

/* --- КНОПКИ (QPushButton) --- */
QPushButton {
	background-color: #F2C73C;
	color: #202124;
	border-radius: 4px;
	padding: 6px 15px;
	font-weight: bold;
	border: none;
}
QPushButton:hover {
	background-color: #F2E167;
}
QPushButton:pressed {
	background-color: #D4A017;
}
QPushButton:disabled {
	background-color: #3c4043;
	color: #80868b;
}

/* --- ПОЛЯ ВВОДА (QLineEdit, QTextEdit) --- */
QLineEdit, QTextEdit, QPlainTextEdit {
	background-color: #303134;
	border: 1px solid #5f6368;
	border-radius: 4px;
	padding: 6px;
	color: #E8EAED;
	selection-background-color: #F2C73C;
	selection-color: #202124;
}
QLineEdit:focus, QTextEdit:focus {
	border: 1px solid #F2C73C;
}

/* Сделаем поле ввода чуть мягче */
QLineEdit {
    border: 1px solid #3c4043;
    background-color: #2d2e31;
    selection-background-color: #F2C73C;
}

/* --- ЧЕКБОКСЫ (QCheckBox) - для Генератора --- */
QCheckBox {
	spacing: 8px;
	color: #E8EAED;
}
QCheckBox::indicator {
	width: 14px;
	height: 14px;
	border: 2px solid #5f6368;
	border-radius: 3px;
	background-color: transparent;
	padding: 2px;
	background-clip: content;
}
QCheckBox::indicator:checked {
	background-color: #F2C73C;
	border: 2px solid #F2C73C;
}
QCheckBox::indicator:hover {
	border: 2px solid #F2E167;
}

/* --- СКРОЛЛБАРЫ (QScrollBar) - чтобы не были серыми --- */
QScrollBar:vertical {
	border: none;
	background: #202124;
	width: 10px;
	margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
	background: #5f6368;
	min-height: 20px;
	border-radius: 5px;
}
QScrollBar::handle:vertical:hover {
	background: #F2C73C;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
	height: 0px;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	background: none;
}

/* --- МЕНЮ (Контекстные меню) --- */
QMenu {
    background-color: #303134;
    border: 1px solid #F2C73C;
    color: #E8EAED;
}
QMenu::item {
    padding: 8px 25px;
}
QMenu::item:selected {
    background-color: #F2C73C;
    color: #202124;
}
QMenu::separator {
    height: 1px;
    background: #3c4043;
    margin: 5px 0px;
}

/* Стрелочка, указывающая на наличие подменю */
QMenu::right-arrow {
    image: url(right_arrow_gold.png);
    width: 10px;
    height: 10px;
    padding-right: 5px;
}

/* Когда мы навели на "Move to", оно должно подсвечиваться золотом */
QMenu::item:selected {
    background-color: #F2C73C;
    color: #202124;
}

/* --- ГРАДИЕНТНЫЙ ТЕКСТ (По ID) --- */
QLabel#GradientLabel {
	color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #F2C73C, stop:1 #F2E167);
	font-weight: bold;
	font-size: 18px;
}

/* --- ОШИБКИ И ПОДСКАЗКИ --- */
QToolTip {
	border: 1px solid #F2C73C;
	background-color: #303134;
	color: #E8EAED;
}

/* Дополнительный стиль для вторичной кнопки (Exit) */
QPushButton#SecondaryBtn {
    background-color: transparent;
    border: 1px solid #5f6368;
    color: #E8EAED;
	margin: 0px;
}
QPushButton#SecondaryBtn:hover {
    border: 1px solid #F2C73C;
    color: #F2C73C;
}

/* Рамка для окна разблокировки */
QWidget#MainContainer {
    background-color: #202124;
    border: 1px solid #F2C73C;
    border-radius: 8px;
}

QComboBox {
    background-color: #303134;
    border: 1px solid #5f6368;
    border-radius: 4px;
    padding: 5px;
    color: #E8EAED;
}

/* Убрали :focus отсюда, теперь после выбора рамка станет серой */
QComboBox:hover, QComboBox:on {
    border: 1px solid #F2C73C;
}

/* Это уберет пунктирную рамку фокуса внутри */
QComboBox {
    outline: none;
}

QPushButton#CloseBtn {
    background-color: transparent;
    border: 1px solid #E63946;
    color: #E63946;
    border-radius: 4px;
    font-weight: bold;
}

QPushButton#CloseBtn:hover {
    background-color: #E63946;
    color: #FFFFFF;
}

/* Универсальное исправление для всех кнопок в таблице, чтобы текст не жал */
QTableWidget QPushButton {
    padding: 4px 8px;
    min-height: 24px;
    line-height: 14px;
    font-size: 13px;
}

/* --- ЦВЕТНЫЕ КНОПКИ В ТАБЛИЦЕ --- */
/* Кнопка COPY (Зеленая) */
QPushButton#CopyBtn {
    background-color: #2ECC71;
    color: #000000;
}
QPushButton#CopyBtn:hover {
    background-color: #58D68D;
}
QPushButton#CopyBtn:pressed {
    background-color: #28B463;
}

/* Кнопка DELETE (Красная) */
QPushButton#DeleteBtn {
    background-color: #E74C3C;
    color: #FFFFFF;
}
QPushButton#DeleteBtn:hover {
    background-color: #EC7063;
}
QPushButton#DeleteBtn:pressed {
    background-color: #C0392B;
}

/* Кнопка SHOW (Оставляем в золотом стиле, но явно укажем) */
QPushButton#ShowBtn {
    background-color: #F2C73C;
    color: #202124;
}
QPushButton#ShowBtn:hover {
    background-color: #F2E167;
}

/* --- СТАТУС-БАР --- */
QLabel#StatusMsg {
    color: #00C853;
    font-weight: bold;
    font-size: 12px;
}

QLabel#BrandingLabel {
    color: #5f6368;
    font-size: 11px;
    font-style: italic;
    padding-right: 5px;
}
"""