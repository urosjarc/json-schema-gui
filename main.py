#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
import json
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPlainTextEdit
from genson import SchemaBuilder
from genson.schema.strategies import List


class MinContains(List):
	# add 'minimum' to list of keywords
	KEYWORDS = (*List.KEYWORDS, 'minContains')

	# create a new instance variable
	def __init__(self, node_class):
		super().__init__(node_class)
		self.minContains = None

	# capture 'minimum's from schemas
	def add_schema(self, schema):
		super().add_schema(schema)
		if self.minContains is None:
			self.minContains = schema.get('minContains')
		elif 'minContains' in schema:
			self.minContains = schema['minContains']

	# adjust minimum based on the data
	def add_object(self, obj):
		super().add_object(obj)
		self.minContains = 1

	# include 'minimum' in the output
	def to_schema(self):
		schema = super().to_schema()
		schema['minContains'] = self.minContains
		return schema


class CustomSchemaBuilder(SchemaBuilder):
	EXTRA_STRATEGIES = (MinContains,)


class Ui(QtWidgets.QMainWindow):
	inputPTE: QPlainTextEdit
	outputPTE: QPlainTextEdit

	def __init__(self):
		super(Ui, self).__init__()
		uic.loadUi('main.ui', self)

		self.inputPTE.textChanged.connect(self.inputChange)

		self.show()

	def inputChange(self):
		try:
			textIn = self.inputPTE.toPlainText()

			builder = CustomSchemaBuilder()
			jsonIn = json.loads(textIn)
			builder.add_object(jsonIn)
			textOut = builder.to_json(indent=4)
			self.outputPTE.setPlainText(textOut)
		except Exception as err:
			self.outputPTE.setPlainText(str(err))


if __name__ == '__main__':

	app = QtWidgets.QApplication(sys.argv)
	window = Ui()
	app.exec_()
