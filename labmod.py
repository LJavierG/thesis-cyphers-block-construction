# -*- coding: utf-8 -*-

"""
Copyright 2015, Luis Javier Gonzalez (luis.j.glez.devel@gmail.com)

This program is licensed under the GNU GPL 3.0 license.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt4.QtCore import Qt, QMimeData
from PyQt4.QtGui import QLabel, QPixmap, QPainter, QColor, QDrag

class labmod(QLabel):

	def __init__(self, name, code = None, parent = None):
		QLabel.__init__(self, name, parent)
		self.code = code
		self.name = name

	def mouseMoveEvent(self, e):
		# Chequear que se esté presionando el botón izquierdo
		if e.buttons() != Qt.LeftButton:
			return

		# posicion del click dentro del gmod
		mimeData = QMimeData()

		pixmap = QPixmap.grabWidget(self)
		painter = QPainter(pixmap)
		painter.setCompositionMode(painter.CompositionMode_DestinationIn)
		painter.fillRect(pixmap.rect(), QColor(0, 0, 0, 127))
		painter.end()

		drag = QDrag(self)
		# escribir el MimeData
		drag.setMimeData(mimeData)
		# establecer el Pixmap
		drag.setPixmap(pixmap)
		# posicionar correctamente el pixmap
		drag.setHotSpot(e.pos())

		drag.exec_(Qt.MoveAction)
