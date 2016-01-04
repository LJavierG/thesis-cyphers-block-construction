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

import re

from PyQt4 import QtCore, QtGui
from links import InConnector, OutConnector
from dialogs import EditDialog

class _Module:

	INT=0
	CHR=1
	BLK=2

	def __init__(self, name, code=None):
		self.name=name
		self.code=code
		self.reset()

	def nargs(self):
		return len(self.args)

	def reset(self):
		self.myFunction = ""
		if self.code != None:
			self.crea(self.code)
		self.res = 0
		self.principal=False
		self.args=[]
		if self.code == None:
			self.num = 0
		else:
			self.num = -1

	def ex(self):
		self.execute()
	def execute(self):
		#ejecuta la funcion asociada con los argumentos establecidos convertidos a formato adecuado
		sandbox = {}
		exec self.myFunction in sandbox
		self.res=eval( "sandbox[\"" + self.name + "\"](" + self.t_args() + ")\n") #"funciones."+self.name+"("+self.t_args()+")")

	def crea(self, code):
		self.myCreate(code)
	def myCreate(self, code):
		if code == None:
			return
		self.code = code
		#crea la funcion a utilizar segun el codigo pasado
		#si se crea mas de una vez la version que se usa es la ultima
		code1=""
		code2=""
		for i in range(0,code.rfind("\n")+1):
			code1+=code[i]
		for i in range(code.rfind("\n")+1,len(code)):
			code2+=code[i]
		if code1 != "":
			code1 += "\n"
		code_fin=code1+"return "+code2
		self.myFunction = "def " + self.name + "(args):\n" + re.sub("^", "\t", code_fin, 0, re.MULTILINE) + "\n"

	def set_args(self, i, m):
		self.setArgs(i,m)
	def setArgs(self, i, m):
		if i>=self.nargs():
			self.args.append(m)
		else:
			self.args[i]=m

	def t_args(self):
		return self.argsToString()
	def argsToString(self):
		cad = "["
		for el in range(self.nargs()):
			if el != 0:
				cad += ","
			cad += str(self.args[el].res)
		cad += "]"
		return cad

	def nom_args(self):
		return self.argsNameToString()
	def argsNameToString(self):
		cad = "["
		for el in range(self.nargs()):
			if el != 0:
				cad += ","
			cad += "v"+str(self.args[el].name)
		cad += "]"
		return cad

	def appendMyFunctionToFile(self, file):
		if self.type != self.Input:
			file.write (re.sub("^", "\t", self.myFunction, 0, re.MULTILINE)+"\n")

	def write_to(self, file):
		self.appendCodeToFile(file)
	def appendCodeToFile(self, file):
		if self.code != None:
			file.write("\tv"+self.name+" = "+self.name+"("+self.nom_args()+")\n")
		else:
			file.write("\tv"+self.name+" = int(args["+ str(self.num) +"])\n")

	def p(self):
		print "res = %r" % self.res

class Module(QtGui.QWidget, _Module):
	Op = 1
	Simple = 2
	Composite = 4
	Input = 8
	Output = 16
	Loop = 32
	Const = 64
	List = 128
	File = 256

	def __init__(self, name, code, parent, cs = None):
		QtGui.QWidget.__init__(self, parent)
		_Module.__init__(self, name, code)

		self.lines = []
		self.type = self.getType(code)
		self.submod = -1
		self.veces = 1
		self.pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

		if self.type == self.Input:
			self.num = self.parent().newInput()
		else:
			self.num = -1

		self.cs = self.parent().cs
		self.createGraphics(self.cs)

	def calculateType(self,code):
		return self.getType(code)
	def getType(self, code):
		if code == None:
			return self.Input
		elif code == "args[0]":
			return self.Output
		elif code.find("times") != -1:
			return self.Loop
		elif code.find("submodel") != -1:
			return self.Composite
		elif code == "":
			return self.Simple
		else:
			return self.Op

	def paintEvent(self, e):
		qp = QtGui.QPainter()
		qp.begin(self)
		self.drawLines(qp)
		qp.end()
		self.raise_()

	def drawLines(self,qp):
		qp.setPen(self.pen)
		qp.drawLine(2,2, 196, 2)
		qp.drawLine(2, 96, 196, 96)
		qp.drawLine(2, 2, 2, 96)
		qp.drawLine(196, 2, 196, 96)

	def crea_graficos(self,cs):
		return self.createGraphics(cs)
	def createGraphics(self, cs):
		self.setGeometry(1,1,200,100)

		# botones de entrada segun el numero de args[i] en code
		self.g_in = []
		i = 0
		if self.type != self.Input and self.type != self.Composite and self.type != self.Loop:
			while True:
				if self.code.find("args["+str(i)+"]") != -1:
					self.g_in.append(InConnector(i,cs,self))
					i+=1
				else:
					break

		if self.type == self.Composite or self.type == self.Loop:
			k=self.parent().entradas_sub_i(self.submod)
			if k != -1:
				for i in range(k):
					self.g_in.append(InConnector(i,cs,self))
				i = k

		self.numar = i

		if i == 0:
			if self.type == self.Input:
				self.g_in = QtGui.QLineEdit("0",self)
				self.g_in.setGeometry(0,0,200,33)
		else:
			h=200/i
			for j in range(i):
				self.g_in[j].setGeometry(j*h,0,h,33)
				self.g_in[j].show()

		self.principal = False
		if self.type == self.Output:
			self.g_out = QtGui.QLabel("*", self)
			self.g_out.setAlignment(QtCore.Qt.AlignCenter)
			self.g_prin = QtGui.QLabel("m",self)
			self.g_prin.setGeometry(180,80,15,15)
			self.g_prin.hide()
			ninguno = 1
			for m in self.parent().modulesList:
				if m.principal:
					ninguno = 0
			if ninguno:
				self.principal = True
				self.g_prin.show()
		else:
			self.g_out= OutConnector(cs, self)

		self.g_out.setGeometry(0,67,200,33)
		self.g_name= QtGui.QLabel(self.name, self)
		self.g_name.setAlignment(QtCore.Qt.AlignCenter)
		self.g_name.setGeometry(34,33,132,34)
		self.g_close= QtGui.QPushButton("x", self)
		self.g_close.setFlat(True)
		self.g_close.setGeometry(166,33,34,34)
		self.g_close.clicked.connect(self.b_close)
		# he decidido permitir la ejecucion individual
		self.g_play= QtGui.QPushButton("p", self)
		self.g_play.clicked.connect(self.b_play)
		self.g_play.setFlat(True)
		self.g_play.setGeometry(0,33,34,34)

		self.g_num = QtGui.QLabel(str(self.num), self)
		self.g_num.setGeometry(180,80,15,15)
		if self.num == -1:
			self.g_num.hide()

	def actualiza_graficos(self):
		return self.updateGraphics()
	def updateGraphics(self):
		g_in = []
		i = 0
		if self.type != self.Input and self.type != self.Composite:
			while True:
				if self.code.find("args["+str(i)+"]") != -1:
					g_in.append(InConnector(i,self.cs,self))
					g_in[-1].hide()
					i+=1
				else:
					break
		#crea un gin por cada entrada en el submodulo.
		if self.type == self.Composite or self.type == self.Loop:
			k=self.parent().entradas_sub_i(self.submod)
			if k != -1:
				for i in range(k):
					g_in.append(InConnector(i,self.cs,self))
					g_in[-1].hide()
				i = k

		if self.numar != i:
			for gin in self.g_in:
				gin.hide()
				for l in self.lines:
					if l.i == gin:
						l.hide()
			self.g_in = g_in[:]
			for el in self.g_in:
				el.show()
			if i == 0:
				if self.type == self.Input:
					self.g_in = QtGui.QLineEdit("0",self)
					self.g_in.setGeometry(0,0,200,33)
			else:
				h=200/i
				for j in range(i):
					self.g_in[j].setGeometry(j*h,0,h,33)
					self.g_in[j].show()
			self.numar = i

		if self.type == self.Output:
			if self.principal:
					self.g_prin.show()
			else:
					self.g_prin.hide()

		self.g_num.setText(str(self.num))

	def b_play(self):
		self.buttonPlay()
	def buttonPlay(self):
		self.g_ex()

	def g_ex(self):
		self.graphicExecute()
	def graphicExecute(self):
		if self.type == self.Input:
			self.res=int(self.g_in.text())
			self.g_out.setText(self.g_in.text())
		elif self.type == self.Composite:
			# TODO gestionar posibles errores, como que el submodulo no este elegido y cosas asi
			db = self.parent().stepparent.models[self.submod]
			for i in range(self.numar):
				db.input(i).g_in.setText(self.args[i].g_out.text())
			db.g_ex()
			res = db.mainOutput().g_out.text()
			self.res= int(res)
			self.g_out.setText(res)
			l = False
		elif self.type == self.Loop:
			r=self.veces
			l=load
			while r != 0:
				db = self.parent().stepparent.sub[self.submod]
				if r == self.veces:
					for i in range(self.numar):
						db.input(i).g_in.setText(self.args[i].g_out.text())
				else:
					db.input(0).g_in.setText(db.main().g_out.text())
				db.g_ex(l)
				self.res = int(db.main().g_out.text())
				self.g_out.setText(db.main().g_out.text())
				l = False
				r -= 1
		else:
			self.ex()
			self.g_out.setText(str(self.res))
		return False

	def outConnect(self):
		self.g_out.connect()

	def inConnect(self, i):
		self.g_in[i].connect()

	def b_close(self):
		self.buttonClose()
	def buttonClose(self):
		# esta funcion en lugar de esconder debe borrar los elementos, actualmente funcionalidad delegada en el recolector de basura
		# y sacar este modulo de la lista del modelo.
		self.hide()
		self.parent().modulesList.remove(self)
		for m in self.parent().modulesList:
			names = [n.name for n in m.args]
			if self.name in names:
				m.args.remove(self)
		if self.num != -1:
			self.parent().delInput(self.num)
		for l in self.lines:
			l.hide()

	def rename(self, new_name):
		"""
		los nombres que se asignan por defecto son
		el nombre de la operacion
		y un numero que les hace de identificador unico.
		el numero lo almaceno segun el numero de modulos
		ya existentes de cada tipo
		"""
		i=0
		name = new_name
		namesList = [m.name for m in self.parent().modulesList if m != self]
		while True:
			if name in namesList:
				name = new_name + "_" + str(i)
				i+=1
			else:
				break
		self.name = name
		self.g_name.setText(name)
		return name

	def mouseDoubleClickEvent(self, e):
		# abre un dialog en el que se pueda editar el modulo
		ed = EditDialog(self)
		ret = ed.exec_()
		if ret == 0:
			return
		else:
			name = ed.ename.text().toLocal8Bit().data()
			self.rename(name)

			if self.type == self.Input:
				tmp = self.num
				num = int(ed.enum.text())
				for m in self.parent().modulesList:
					if m.num == num:
						m.num = tmp
						self.num = num
						break
			elif self.type == self.Output:
				if ed.lprin.isChecked():
					ex_p = self.parent().mainOutput()
					ex_p.principal = False
					ex_p.actualiza_graficos()
					self.principal = True
			elif self.type == self.Composite or self.type == self.Loop:
				# contar entradas del submodelo y crear esas entradas.
				c = ed.esub.currentText().toLocal8Bit()
				self.code = c.data() + "(args)"
				self.submod = ed.esub.currentIndex()
				if self.type == self.Loop:
					self.veces = int(ed.enum.text())
					self.code = "\tfor times in range(" + str(self.veces) + "):\n\t\tret=" + self.code + "\n\t\targs[0]=ret\nret"
				self.crea(self.code)
			elif self.type == self.Simple or self.type == self.Op:
				c = ed.ecode.toPlainText().toLocal8Bit()
				self.code = c.data()
				self.crea(self.code)
			self.actualiza_graficos()

	def mouseMoveEvent(self, e):
		# Chequear que se esté presionando el botón izquierdo
		if e.buttons() != QtCore.Qt.LeftButton:
			return

		# posicion del click dentro del gmod
		mimeData = QtCore.QMimeData()
		mimeData.setText('%d,%d' % (e.x(), e.y()))

		pixmap = QtGui.QPixmap.grabWidget(self)
		painter = QtGui.QPainter(pixmap)
		painter.setCompositionMode(painter.CompositionMode_DestinationIn)
		painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
		painter.end()

		drag = QtGui.QDrag(self)
		# put our MimeData
		drag.setMimeData(mimeData)
		# set its Pixmap
		drag.setPixmap(pixmap)
		# posicionar correctamente el pixmap
		drag.setHotSpot(e.pos())

		drag.exec_(QtCore.Qt.MoveAction)

