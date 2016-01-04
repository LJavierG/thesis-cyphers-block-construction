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

from PyQt4.QtGui import QScrollArea, QTabWidget, QTabBar, QMessageBox
from PyQt4.QtCore import pyqtSlot

from dropframe import DropFrame
from module import Module
from dialogs import NameDialog

import os
import json

class MyTabBar(QTabBar):
	def __init__(self, parent=None):
		QTabBar.__init__(self,parent)

	def mouseDoubleClickEvent(self, e):
		id = self.tabAt(e.pos())
		dia = NameDialog(self.tabText(id))
		if dia.exec_():
			try:
				self.parent().renameModel(self.tabText(id), dia.ename.text().toLocal8Bit().data())
			except:
				QMessageBox.question(self, 'Message', "Nombre ya en uso.", QMessageBox.Ok)
				self.parent().say("Error al intentar cambiar el nombre")
				return
			self.setTabText(id, dia.ename.text())

class Central(QTabWidget):
	def __init__(self, parent=None):
		QTabWidget.__init__(self, parent)
		self.reset()
		self.setTabBar(MyTabBar(self))
		self.setTabsClosable(True)

	@pyqtSlot()
	def reset(self):
		self.clear()
		self.empty = True
		self.models = []
		self.parent().emptied()

	@pyqtSlot()
	def newTab(self,name=None):
		scroll = QScrollArea(self)
		if name == None:
			name = "modelo_"+str(len(self.models))
			i=1
			while name in [ m.name for m in self.models ]:
				name = "modelo_"+str(len(self.models)+i)
				i+=1

		self.models.append(DropFrame(name, self))
		self.models[-1].setGeometry(0,0,3000,2000)
		scroll.setWidget(self.models[-1])
		self.addTab(scroll, self.models[-1].name)
		self.empty = False

	@pyqtSlot()
	def execute(self):
		if len(self.models) > 0:
			self.models[0].g_ex()

	@pyqtSlot()
	def build(self):
		if len(self.models) > 0:
			self.models[0].g_build()

	def renameModel(self, old_name, new_name):
		if new_name in [el.name for el in self.models]:
			raise Exception
		for el in self.models:
			if el.name == old_name:
				el.name = new_name
				return

	@pyqtSlot()
	def saveJSON(self):
		if not self.empty:
			try:
				self.save_json(self.parent().fichero)
				self.say("Modelo guardado con exito")
			except:
				self.say("Error al guardar el modelo")

	@pyqtSlot()
	def loadJSON(self):
		try:
			self.load_json(self.parent().fichero)
			self.say("Modelo cargado con exito")
		except:
			self.say("Error al cargar el modelo")

	@pyqtSlot(str)
	def importJSON(self,s):
		try:
			self.import_json(s)
			self.say("Modulo añadido con exito")
		except:
			self.say("Error al añadir el modulo")

	@pyqtSlot(str)
	def exportJSON(self,s):
		try:
			self.export_json(s)
			self.say("Modulo exportado con exito")
		except:
			self.say("Error al exportar el modulo")

	def say(self, txt):
		self.parent().say(txt)

	def save_json(self, filename):
		data = {}
		for i in range(len(self.models)):
			data = self.append_model(data,i)
		f = open(filename, "w")
		f.write(json.dumps(data))
		f.close()

	def append_model(self, data, modelnum):
		k=str(modelnum)
		if data == {}:
			k="0"
		data[k]={"name" : self.models[modelnum].name}
		for el in range(len(self.models[modelnum].modulesList)):
			data[k] = self.append_module(data[k], modelnum, el)
		return data

	def append_module(self, data, modelnum, el):
		m = self.models[modelnum].modulesList[el]
		data[str(el)]={"name" : m.name, "type" : m.type, "pos" : { "x" : m.pos().x(), "y" : m.pos().y() }, "code" : m.code, "veces" : m.veces, "num": m.num, "submod": m.submod, "principal" : m.principal}
		ar={}
		for a in range(len(m.args)):
			ar[str(a)] = m.args[a].name
		data[str(el)]["args"] = ar
		return data

	def export_json(self, filename):
		data={}
		data = self.append_model(data, self.currentIndex())
		f = open(filename, "w")
		f.write(json.dumps(data))
		f.close()

	def load_json(self, filename):
		self.reset()
		self.import_json(filename)

	def import_json(self,filename):
		f = open(filename, "r")
		d = json.load(f)
		f.close()
		ll=len(list(d.keys()))
		for i in range(ll):
			self.newTab(d[str(i)]["name"])
			self.load_model(d[str(i)],self.models[i])
		self.models[0].update_composite()
		for i in range(ll):
			self.connect_model(d[str(i)],self.models[i])

	def load_model(self, dic, db):
		#CORREGIDO esta funcion no esta cargando correctamente el submodelo que tenia asociado un compuesto y por extension un bucle
		# creo que es porque no se guarda correctamente el json y tampoco se carga aqui.
		del dic["name"]
		for m in dic.values():
			m2 = Module(m["name"], m["code"] if m["code"]!="null" else None, db)
			if "type" in m.keys():
				m2.type = m["type"]
			m2.move(m["pos"]["x"],m["pos"]["y"])
			m2.principal = m["principal"]
			m2.num = m["num"]
			m2.submod = m["submod"]
			m2.veces = m["veces"]
			m2.show()
			m2.actualiza_graficos()
			db.addModule(m2)

	def connect_model(self, dic, db):
		for m in dic.values():
			for i in range(len(m["args"].keys())):
				db.module_named(m["args"][str(i)]).outConnect()
				db.module_named(m["name"]).inConnect(i)
