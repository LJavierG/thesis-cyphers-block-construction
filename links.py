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

from PyQt4.QtCore import Qt, QPoint
from PyQt4.QtGui import QPushButton, QWidget, QPainter, QPen

class Connector(QPushButton):

	IO = None
	In = 1
	Out= 2

	def __init__(self, num, cs, parent):
		QPushButton.__init__(self, "*", parent)
		self.setFlat(True)
		self.connected = False
		self.cs = cs
		self.type = self.IO
		self.num = num
		self.clicked.connect(self.connect)

	def con(self, c):
		c.connected=True
		c.setText("o")

	def connect(self):
		if self.cs.state == None:
			self.cs.state = self
		elif self.cs.state.type == self.type:
			self.cs.state = self
		else:
			if self.type == self.In:
				self.con(self)
				self.parent().set_args(self.num,self.cs.state.parent())
				for l in self.parent().lines:
					if l.i == self:
						l.hide()
			elif self.type == self.Out:
				self.con(self.cs.state)
				self.cs.state.parent().set_args(self.cs.state.num,self.parent())
				for l in self.cs.state.parent().lines:
					if l.i == self.cs.state:
						l.hide()
			l = Line(self, self.cs.state, self.parent().parent())
			self.parent().lines.append(l)
			self.cs.state.parent().lines.append(l)
			self.cs.state = None
		return 0

class LinkCreator:
	def __init__(self):
		self.state = None

class InConnector(Connector):
	def __init__(self, num, cs, parent):
		Connector.__init__(self, num, cs, parent)
		self.type = self.In

	def isConnected(self):
		return self.connected

class OutConnector(Connector):
	def __init__(self, cs, parent):
		Connector.__init__(self, 0, cs, parent)
		self.type = self.Out

class Line(QWidget):
	def __init__(self, i, f, parent):
		QWidget.__init__(self, parent)
		# i y f son el conector inicial y el final de la linea
		if i.type == i.In:
			self.i = i
			self.f = f
		else:
			self.i = f
			self.f = i
		self.setGeometry(0, 0, 1280, 1270)
		self.show()
		self.lower()

	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawLine(qp)
		qp.end()

	def drawLine(self, qp):
		posi = self.i.pos()+self.i.parent().pos()+QPoint(self.i.size().width()/2,0)
		posf = self.f.pos()+self.f.parent().pos()+QPoint(100,31)

		pen = QPen(Qt.black, 2, Qt.SolidLine)
		qp.setPen(pen)
		qp.drawLine(posi, posf)
