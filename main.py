#!/usr/bin/python2.7
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

from sys import argv
from PyQt4.QtGui import QApplication, QMainWindow, QShortcut, QCloseEvent, QMessageBox
from PyQt4.QtCore import Qt, QSettings, pyqtSlot

from central_widget import Central
from docks import DockTools, DockFileSystem
from menu_widget import Menu

class MainWindow(QMainWindow):

	Empty = 1
	Unsaved = 2
	Saved = 3

	def __init__(self):
		self.setup()
		self.createDocks()
		self.createCentral()
		self.createMenus()
		self.createShortcuts()
		self.readSettings()
		self.show()
		self.say("Carga completada")

	def setup(self):
		QMainWindow.__init__(self)
		self.setWindowTitle("Criptocefa")
		self.state = self.Empty
		self.fichero = None
		self.workdir = "./"
		#self.showMaximized()

	def createMenus(self):
		self.setMenuBar(Menu(self))
		self.menuBar().newpage.connect(self.centralWidget().newTab)
		self.menuBar().save.connect(self.centralWidget().saveJSON)
		self.menuBar().load.connect(self.centralWidget().loadJSON)
		self.menuBar().mod_import.connect(self.centralWidget().importJSON)
		self.menuBar().mod_export.connect(self.centralWidget().exportJSON)
		self.menuBar().reset.connect(self.centralWidget().reset)
		self.menuBar().play.connect(self.centralWidget().execute)
		self.menuBar().build.connect(self.centralWidget().build)
		self.menuBar().exit.connect(self.close)

	def createShortcuts(self):
		QShortcut(Qt.Key_F5,self.centralWidget(),self.centralWidget().execute)
		QShortcut(Qt.Key_F6,self.centralWidget(),self.centralWidget().build)

	def createDocks(self):
		self.addDockWidget(DockTools.left, DockTools(self))
		self.addDockWidget(DockTools.right, DockFileSystem(self))

	def createCentral(self):
		self.setCentralWidget(Central(self))

	@pyqtSlot()
	def closeEvent(self, e):
		"""
		if self.state == self.Unsaved:
			cad = u"Esta a punto de salir sin guardar, ¿salir?"
			reply = QMessageBox.question(self, 'Message', cad, QMessageBox.Yes, QMessageBox.No)
			if reply == QMessageBox.No:
				e.ignore()
				return
		"""
		
		#Vaciamos el proyecto antes de cerrar la aplicacion.
		self.centralWidget().reset()
		
		settings = QSettings("LuisjaCorp", "Criptocefa")
		settings.setValue("geometry", self.saveGeometry())
		settings.setValue("windowState", self.saveState())
		
		QMainWindow.closeEvent(self, e)

	def readSettings(self):
		settings = QSettings("LuisjaCorp", "Criptocefa")
		self.restoreGeometry(settings.value("geometry").toByteArray())
		self.restoreState(settings.value("windowState").toByteArray())

	def edited(self):
		self.state = self.Unsaved

	def saved(self):
		self.state = self.Saved

	def emptied(self):
		self.state = self.Empty

	def isUnsaved(self):
		if self.state == self.Unsaved:
			return True
		else:
			return False

	def say(self, txt):
		self.statusBar().showMessage(txt,0)

#if __name__ == "__main__":
app = QApplication(argv)
ventana = MainWindow()
ventana.show()
app.exec_()
