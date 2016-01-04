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

from PyQt4 import QtCore
from PyQt4 import QtGui

from module import Module
from links import LinkCreator

class Model:
	def __init__(self, name):
		self.name=name
		self.modulesList=[]

	def numModules(self):
		return len(self.modulesList)

	def addModule(self, m):
		self.modulesList.append(m)

	def newModule(self, name, code):
		self.addModule(Module(name, code))

	def module_named(self, cad):
		return self.moduleNamed(cad)
	def moduleNamed(self, cad):
		for el in self.modulesList:
			if el.name == cad:
				return el

	def execute(self):
		lista=self.sortedList()
		for m in lista:
			m.execute()

	def sortedList(self):
		"""
		retorna una lista con los modulos ordenados para ejecucion o construccion del codigo
		es una variante de ordenacion topologica adaptada a mi estructura de modelos y modulos.
		"""
		lista=[]
		ingrade={}
		lista_inicial=self.modulesList[:]
		#ahora calculo los grados de entrada
		for m in lista_inicial:
			ingrade[m] = len(m.args)
		#y con esos grados voy poniendo en la lista final los que tengan 0, reduzco aquellos en que incide y vuelvo a sacar los que tienen 0
		while len(lista_inicial)>0:
			borrar=[]
			for m in lista_inicial:
				if ingrade[m]==0:
					borrar.append(m)
					for n in lista_inicial:
						if m in n.args:
							ingrade[n] -= n.args.count(m)
			lista.extend(borrar)
			for el in borrar:
				lista_inicial.remove(el)
		return lista

	def codeToFile(self, file):
		"""escribe en file el codigo en python para que este modelo se ejecute y funcione de manera normal"""
		file.write("def "+ self.name + "(args):\n")
		lista=self.sortedList()
		for m in lista:
			m.appendMyFunctionToFile(file)
		for m in lista:
			m.write_to(file)
		file.write("\treturn v"+lista[-1].name+"\n\n")


class DropFrame(QtGui.QFrame, Model):

	def __init__(self, name, parent):
		QtGui.QFrame.__init__(self, parent)
		Model.__init__(self, name)

		self.setAcceptDrops(True)
		self.entradas = 0
		self.stepparent = parent
		self.cs = LinkCreator()

	def g_ex(self, load = True):
		self.graphicExecute()
	def graphicExecute(self):
		lista=self.sortedList()

		for m in lista:
			m.g_ex()
		self.say("Ejecucion completada con exito")

	def newInput(self):
		ent=self.entradas
		self.entradas+=1
		return ent

	def delInput(self, num):
		for m in self.modulesList:
			if m.num > num:
				m.num -= 1
		self.entradas -= 1
		self.update_composite()

	def g_build(self):
		self.graphicBuild()
	def graphicBuild(self):
		fichname = self.name + ".py"
		f=open(fichname, "w")
		for m in self.stepparent.models:
			m.codeToFile(f)
		f.write("if __name__ == '__main__':\n\tfrom sys import argv\n\tprint "+self.name+"(argv[1:])")
		f.close()
		self.say("Codigo contruido a partir del modelo con exito")

	def input(self, i):
		for m in self.modulesList:
			if m.num == i:
				return m

	def mainOutput(self):
		for m in self.modulesList:
			if m.principal:
				return m

	def entradas_sub_i(self, i):
		return self.inputsOfModel(i)
	def inputsOfModel(self,num):
		try:
			val = self.stepparent.models[num].entradas
		except:
			val = -1
		return val

	def update_composite(self):
		return self.updateComposite()
	def updateComposite(self):
		for s in self.stepparent.models:
			for m in s.modulesList:
				if m.type == Module.Composite or m.type == Module.Loop:
					m.actualiza_graficos()

	def dragEnterEvent(self, e):
		e.accept()

	def newName(self, base):
		i=0
		name = base
		namesList = [m.name for m in self.modulesList]
		while True:
			if name in namesList:
				name = base + "_" + str(i)
				i+=1
			else:
				return name

	def dropEvent(self, e):
		# Establecer el widget en una nueva posición
		# aqui tengo que separar entre modulos nuevos y ya existentes.
		# la cadena que transmito es "posx,posy" si es mover uno existe
		# posx y posy es la posicion relativa al modulo del cursor
		# los ya existentes, muevo el modulo que paso con el drag a
		# la posicion del click menos el punto (posx,posy)
		# los modulos nuevos, hago una copia de ese tipo de modulo
		# de una base que no se este mostrando, y lo muestro
		# y no solo eso, sino que ademas mantengo
		# la numeracion de cada tipo de modulos para generar siguientes

		# obtiene la posicion relativa de los datos mime (mimeData)
		if e.mimeData().hasText():
			x, y = map(int, e.mimeData().text().split(','))
			e.source().move(e.pos()-QtCore.QPoint(x, y))
			e.setDropAction(QtCore.Qt.MoveAction)
			for l in e.source().lines:
				l.repaint()
		else:
			name=self.newName(e.source().name)
			m = Module(name, e.source().code, self)
			m.move(e.pos()-QtCore.QPoint(100,50))
			m.show()
			self.addModule(m)
			if m.type == Module.Input:
				self.update_composite()
			e.setDropAction(QtCore.Qt.CopyAction)
		e.accept()

	def say(self, txt):
		self.stepparent.say(txt)
