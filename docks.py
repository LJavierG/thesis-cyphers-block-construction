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

from PyQt4.QtGui import QDockWidget, QToolBox, QWidget, QVBoxLayout, QFileSystemModel, QTreeView, QLineEdit, QPushButton, QFileDialog, QHBoxLayout
from PyQt4.QtCore import Qt, pyqtSlot

from labmod import labmod

class DockTools(QDockWidget):

	left = Qt.LeftDockWidgetArea
	right = Qt.RightDockWidgetArea

	def __init__(self, parent = None):
		QDockWidget.__init__(self, "Herramientas", parent)
		self.setObjectName("ToolBoxDock")

		self.setAllowedAreas( self.left | self.right )
		self.setGeometry(0,0,200,1000)

		tb = QToolBox(self)
		#esta es la manera de crear una nueva entrada para toolbox
		##BASICOS
		widget_ba = QWidget(self)
		caja_ba = QVBoxLayout(widget_ba)
		widget_ba.setLayout(caja_ba)
		tb.addItem(widget_ba, "Modulos basicos")
		caja_ba.addWidget(labmod("Entrada"))
		caja_ba.addWidget(labmod("Salida", "args[0]"))
		caja_ba.addWidget(labmod("Simple", ""))
		caja_ba.addWidget(labmod("Compuesto", "submodel"))
		caja_ba.addWidget(labmod("Bucle", "times"))

		##OPERACIONES BASICAS
		widget_op = QWidget(self)
		caja_op = QVBoxLayout(widget_op)
		widget_op.setLayout(caja_op)
		tb.addItem(widget_op, "Op elementales")
		#esta es la forma de añadir un nuevo toolbutton al toolbox en un desplegable en concreto
		caja_op.addWidget(labmod("Suma", "args[0]+args[1]"))
		caja_op.addWidget(labmod("Resta", "args[0]-args[1]"))
		caja_op.addWidget(labmod("Producto", "args[0]*args[1]"))
		caja_op.addWidget(labmod("Division", "args[0]/args[1]"))
		caja_op.addWidget(labmod("Resto", "args[0]%args[1]"))
		caja_op.addWidget(labmod("Sustitucion", "V = [1,2,3]\nV[args[0]%len(V)]"))

		#OPERACIONES A NIVEL DE BIT
		widget_bit  = QWidget(self)
		caja_bit = QVBoxLayout(widget_bit)
		widget_bit.setLayout(caja_bit)
		tb.addItem(widget_bit, "Op a nivel de bit")
		caja_bit.addWidget(labmod("AND", "args[0]&args[1]"))
		caja_bit.addWidget(labmod("OR", "args[0]|args[1]"))
		caja_bit.addWidget(labmod("XOR", "args[0]^args[1]"))
		caja_bit.addWidget(labmod("NOT", "~args[0]"))
		caja_bit.addWidget(labmod("DesplazaIzda", "args[0]<<args[1]"))
		caja_bit.addWidget(labmod("DesplazaDcha", "args[0]>>args[1]"))
		caja_bit.addWidget(labmod("RotacionIzda", "def f(n,d,b):\n\tm=0\n\tfor el in range(b):\n\t\tm+=1<<el\n\tfor el in range(d):\n\t\tn=((n<<1)&m)+(((n<<1)&(1<<b))>>(b))\n\treturn n\nf(args[0],args[1],args[2])"))
		caja_bit.addWidget(labmod("RotacionDcha", "def f(n,d,b):\n\tfor el in range(d):\n\t\tn=(n>>1)+((n&1)<<(b-1))\n\treturn n\nf(args[0],args[1],args[2])"))
		caja_bit.addWidget(labmod("Permutacion", "def f(argv):\n\tv=argv[0]\n\tv=v>>argv[1]\n\tv=v&1\n\treturn v\nV=[4,3,2,1]\nt=0\nfor i in range(len(V)):\n\tt+=(f([args[0], V[i]-1])<<i)\nt"))

		#OPERACIONES MODULARES
		widget_bit  = QWidget(self)
		caja_bit = QVBoxLayout(widget_bit)
		widget_bit.setLayout(caja_bit)
		tb.addItem(widget_bit, "Op modulares")
		caja_bit.addWidget(labmod("SumaM", "(args[0]+args[1])%args[2]"))
		caja_bit.addWidget(labmod("MultiplicacionM", "(args[0]*args[1])%args[2]"))
		caja_bit.addWidget(labmod("ExponenciacionM", "g=args[0]\nu=args[1]\np=args[2]\ns = 1\nwhile u != 0:\n\tif u & 1:\n\t\ts = (s * g)%p\n\tu >>= 1\n\tg = (g * g)%p\ns"))
		caja_bit.addWidget(labmod("InversoM", "a,b,s,t,s1,t1= [args[0],args[1],1,0,0,1]\nwhile(b!=0):\n\tq,r=[a/b,a%b]\n\ta,sa=[b,s]\n\ts,ta=[s1,t]\n\tt,b=[t1,r]\n\ts1,t1=[sa-s1*q,ta-t1*q]\nwhile (s<=0):\n\ts+=args[1]\ns"))

		dockbox = QWidget(self)
		vl = QVBoxLayout(dockbox)
		dockbox.setLayout(vl)
		vl.addWidget(tb)
		self.setWidget(dockbox)

		self.adjustSize()

		self.parent().say("Caja de herramientas creada")

class DockFileSystem(QDockWidget):

	left = Qt.LeftDockWidgetArea
	right = Qt.RightDockWidgetArea

	def __init__(self, parent = None):
		QDockWidget.__init__(self, "File System Tree View", parent)
		self.setObjectName("FileNavigatorDock")

		self.fsm = QFileSystemModel(self)
		tv = QTreeView(self)
		tv.showColumn(1)
		self.fsm.setRootPath(self.parent().workdir)
		tv.setModel(self.fsm)

		self.setAllowedAreas( self.left | self.right )
		self.setGeometry(0,0,400,1000)

		pb = QPushButton("...",self)
		pb.clicked.connect(self.changeWorkdir)
		self.le = QLineEdit(self)
		self.le.setText(self.parent().workdir)

		dockbox = QWidget(self)
		hl = QHBoxLayout(dockbox)
		hl.addWidget(self.le)
		hl.addWidget(pb)
		hll=QWidget(self)
		hll.setLayout(hl)
		vl = QVBoxLayout(dockbox)
		dockbox.setLayout(vl)
		vl.addWidget(hll)
		vl.addWidget(tv)
		self.setWidget(dockbox)

		self.adjustSize()

		self.parent().say("Vista del sistema de ficheros creada")

	@pyqtSlot()
	def changeWorkdir(self):
		dialog=QFileDialog(self,"Elige directorio de trabajo",self.parent().workdir)
		dialog.setFileMode(QFileDialog.Directory)
		dialog.setAcceptMode(QFileDialog.AcceptOpen)
		if dialog.exec_():
			fichero = dialog.selectedFiles().first().toLocal8Bit().data()
			self.parent().workdir = fichero
			self.le.setText(fichero)
			self.fsm.setRootPath(self.parent().workdir)

