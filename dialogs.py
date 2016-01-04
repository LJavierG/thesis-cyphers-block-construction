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

from PyQt4.QtGui import QDialog, QGridLayout, QLabel, QLineEdit, QComboBox, QPushButton, QCheckBox, QTextEdit

class EditDialog(QDialog):
	def __init__(self,parent = None):
		QDialog.__init__(self,parent)

		self.setGeometry(200,300,500,300)

		l = QGridLayout(self)

		self.setLayout(l)

		lname = QLabel("name", self)
		self.ename = QLineEdit(self)
		self.ename.setText(self.parent().name)
		l.addWidget(lname, 1,1)
		l.addWidget(self.ename, 1,2)

		if self.parent().type == self.parent().Output:
			self.lprin = QCheckBox("Main output", self)
			self.lprin.setChecked(self.parent().principal)
			#self.eprin = QLineEdit(self)
			#self.eprin.setText(self.parent().code)
			l.addWidget(self.lprin, 2,2)
			#l.addWidget(self.ecode, 2,2)
		elif self.parent().type == self.parent().Input:
			lnum = QLabel("Input number", self)
			self.enum = QLineEdit(self)
			self.enum.setText(str(self.parent().num))
			l.addWidget(lnum, 2,1)
			l.addWidget(self.enum, 2,2)
		elif self.parent().type == self.parent().Composite:
			lsub = QLabel("Submodel:", self)
			self.esub = QComboBox(self)
			for it in self.parent().parent().stepparent.models:
				self.esub.addItem(it.name)
			self.esub.setCurrentIndex(self.parent().submod)
			l.addWidget(lsub, 2,1)
			l.addWidget(self.esub, 2,2)
		elif self.parent().type == self.parent().Loop:
			lsub = QLabel("Submodel:", self)
			self.esub = QComboBox(self)
			for it in self.parent().parent().stepparent.models:
				self.esub.addItem(it.name)
			self.esub.setCurrentIndex(self.parent().submod)
			l.addWidget(lsub, 2,1)
			l.addWidget(self.esub, 2,2)
			lnum = QLabel("Times:", self)
			self.enum = QLineEdit(self)
			self.enum.setText(str(self.parent().veces))
			l.addWidget(lnum, 3,1)
			l.addWidget(self.enum, 3,2)
		else:
			lcode = QLabel("Code", self)
			self.ecode = QTextEdit(self)
			self.ecode.setText(self.parent().code)
			l.addWidget(lcode, 2,1)
			l.addWidget(self.ecode, 2,2)

		ok = QPushButton("Ok", self)
		ok.clicked.connect(self.accept)
		l.addWidget(ok, 4,1)
		cancel = QPushButton("Cancel", self)
		cancel.clicked.connect(self.reject)
		l.addWidget(cancel, 4,2)


class UnsavedDialog(QDialog):
	def __init__(self,parent = None):
		QDialog.__init__(self,parent)
		self.setGeometry(200,300,500,200)
		l = QGridLayout(self)
		self.setLayout(l)

		lname = QLabel("El modelo actual no se ha guardado, continuar de todas formas?", self)
		l.addWidget(lname, 1,1)

		ok = QPushButton("Yes", self)
		ok.clicked.connect(self.accept)
		l.addWidget(ok, 2,1)
		cancel = QPushButton("No", self)
		cancel.clicked.connect(self.reject)
		l.addWidget(cancel, 3,1)

class NameDialog(QDialog):
	def __init__(self,text="",parent = None):
		QDialog.__init__(self,parent)

		self.setGeometry(200,300,500,300)

		l = QGridLayout(self)
		self.setLayout(l)

		lname = QLabel("Name", self)
		self.ename = QLineEdit(self)
		self.ename.setText(text)
		l.addWidget(lname, 1,1)
		l.addWidget(self.ename, 1,2)

		ok = QPushButton("Ok", self)
		ok.clicked.connect(self.accept)
		l.addWidget(ok, 4,1)
		cancel = QPushButton("Cancel", self)
		cancel.clicked.connect(self.reject)
		l.addWidget(cancel, 4,2)

