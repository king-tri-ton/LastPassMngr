from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class DraggableMixin:

	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			self._edge_margin = 15
			pos = event.position().toPoint()
			rect = self.rect()

			self._resizing_x = pos.x() > rect.width() - self._edge_margin
			self._resizing_y = pos.y() > rect.height() - self._edge_margin

			if self._resizing_x or self._resizing_y:
				self._drag_pos = event.globalPosition().toPoint()
				self._start_geometry = self.geometry()
			else:
				self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
			event.accept()

	def mouseMoveEvent(self, event):
		pos = event.position().toPoint()
		rect = self.rect()
		margin = 15

		on_right = pos.x() > rect.width() - margin
		on_bottom = pos.y() > rect.height() - margin

		if on_right and on_bottom:
			self.setCursor(QCursor(Qt.CursorShape.SizeFDiagCursor))
		elif on_right:
			self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
		elif on_bottom:
			self.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
		else:
			self.unsetCursor()

		if event.buttons() & Qt.MouseButton.LeftButton:

			if hasattr(self, '_resizing_x') and (self._resizing_x or self._resizing_y):
				diff = event.globalPosition().toPoint() - self._drag_pos
				new_width = self._start_geometry.width() + (diff.x() if self._resizing_x else 0)
				new_height = self._start_geometry.height() + (diff.y() if self._resizing_y else 0)
				self.resize(max(800, new_width), max(333, new_height))
			else:
				if hasattr(self, '_drag_pos'):
					self.move(event.globalPosition().toPoint() - self._drag_pos)
			event.accept()

	def mouseReleaseEvent(self, event):
		self._resizing_x = False
		self._resizing_y = False
		self.unsetCursor()
