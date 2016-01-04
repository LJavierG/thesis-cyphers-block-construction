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

from PyQt4.QtGui import QMenuBar, QFileDialog
from PyQt4.QtCore import pyqtSignal, pyqtSlot
from dialogs import UnsavedDialog as unsaved_dialog

class Menu(QMenuBar):

	"""
	Menu incompleto, los menus editar, vistas, opciones y ayuda estan de decoracion de momento.
	Archivo		Editar 			Ejecucion	Vistas 		Opciones		Ayuda
	Nuevo		Copiar			play		show/hide 	Terminal		About
	Abrir		Pegar		  	build		docks		Configuracion	Tutorial
	Guardar		Selec. todo	  				menu
	Cerrar									zoom
	---------
	5 ultimos
	---------
	Salir
	"""
	newpage = pyqtSignal()
	save = pyqtSignal()
	load = pyqtSignal()
	reset = pyqtSignal()
	mod_import = pyqtSignal(str)
	mod_export = pyqtSignal(str)
	play = pyqtSignal()
	build = pyqtSignal()
	exit = pyqtSignal()

	def __init__(self, parent):
		QMenuBar.__init__(self, parent)

		file = self.addMenu("&Archivo")
		n = file.addAction("&Nuevo Modelo")
		n.triggered.connect(self.trigger_new)
		n = file.addAction("Nueva &Pagina")
		n.triggered.connect(self.trigger_newpage)
		n = file.addAction("A&brir Modelo")
		n.triggered.connect(self.load_dialog)
		n = file.addAction("&Guardar Modelo")
		n.triggered.connect(self.save_as_dialog)

		n = file.addAction("&Importar Modulo")
		n.triggered.connect(self.get_from_fich)
		n = file.addAction("E&xportar Modulo")
		n.triggered.connect(self.put_to_fich)

		n = file.addAction("&Cerrar Modelo")
		n.triggered.connect(self.trigger_reset)
		file.addSeparator()
		n = file.addAction("&Salir")
		n.triggered.connect(self.exit.emit)
		

		edit = self.addMenu("&Editar")

		ex = self.addMenu("Ejecuc&ion")
		n = ex.addAction("E&jecutar")
		n.triggered.connect(self.play.emit)
		n = ex.addAction("&Construir")
		n.triggered.connect(self.build.emit)

		#view = self.addMenu("V&istas")

		opt = self.addMenu("&Opciones")

		help = self.addMenu("Ay&uda")
		help.addAction("&Tutorial")
		help.addAction("Sobre el autor")
		help.addAction("Sobre la aplicacion")

		self.parent().say("Menu creado")

	@pyqtSlot()
	def trigger_new(self):
		if not self.parent().isUnsaved():
			self.new_nodialog()
		else:
			uns = unsaved_dialog(self)
			if uns.exec_():
				self.new_nodialog()

	@pyqtSlot()
	def trigger_reset(self):
		if not self.parent().isUnsaved():
			self.reset.emit()
		else:
			uns = unsaved_dialog(self)
			if uns.exec_():
				self.reset.emit()

	def new_nodialog(self):
		self.reset.emit()
		self.newpage.emit()
		self.parent().edited()

	@pyqtSlot()
	def trigger_newpage(self):
		self.newpage.emit()
		self.parent().edited()

	@pyqtSlot()
	def save_nodialog(self):
		if (self.parent().fichero != None):
			self.save.emit()
			self.parent().saved()

	@pyqtSlot()
	def save_as_dialog(self):
		dialog=QFileDialog(self,"Guardar Modelo",self.parent().workdir,"Modelos Criptocefa (*.json)")
		dialog.setAcceptMode(QFileDialog.AcceptSave)
		if self.parent().fichero != None:
			dialog.selectFile(self.parent().fichero)
		if (dialog.exec_()):
			self.parent().fichero = dialog.selectedFiles().first().toLocal8Bit().data()
			if (self.parent().fichero.find(".json")==-1):
				self.parent().fichero+=".json"
			self.save_nodialog()

	@pyqtSlot()
	def load_dialog(self):
		if not self.parent().isUnsaved():
			self.load_base()
		else:
			uns = unsaved_dialog(self)
			if uns.exec_():
				self.load_base()

	def load_base(self):
		dialog=QFileDialog(self,"Abrir Modelo",self.parent().workdir,"Modelos Criptocefa (*.json)")
		dialog.setAcceptMode(QFileDialog.AcceptOpen)
		if dialog.exec_():
			self.parent().fichero = dialog.selectedFiles().first().toLocal8Bit().data()
			if self.parent().fichero.find(".json") == -1:
				mm = self.parent().fichero.rfind(".")
				self.parent().fichero = self.parent().fichero[0:mm+1] + "json"
			self.load.emit()
			self.parent().saved()

	@pyqtSlot()
	def get_from_fich(self):
		dialog=QFileDialog(self,"Abrir Modulo",self.parent().workdir,"Modelos Criptocefa (*.json)")
		dialog.setAcceptMode(QFileDialog.AcceptOpen)
		if dialog.exec_():
			fichero = dialog.selectedFiles().first().toLocal8Bit().data()
			self.mod_import.emit(fichero)
			self.parent().edited()

	@pyqtSlot()
	def put_to_fich(self):
		dialog=QFileDialog(self,"Guardar Modulo",self.parent().workdir,"Modelos Criptocefa (*.json)")
		dialog.setAcceptMode(QFileDialog.AcceptSave)
		if dialog.exec_():
			fichero = dialog.selectedFiles().first().toLocal8Bit().data()
			if (fichero.find(".json")==-1):
				fichero+=".json"
			self.mod_export.emit(fichero)

