from PyQt6.QtWidgets import (
	QWidget,
	QLineEdit,
	QHBoxLayout,
	QVBoxLayout,
	QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator,QDoubleValidator


class LabelEditText(QWidget):
	def __init__(self, displayString, validator = None, defaultInput = ""):
		super().__init__()

		self.input = defaultInput
		self.displayString = displayString

		### horizontal layout (Input)
		h_layout = QHBoxLayout(self)

		#### textview says "Sticer name"
		labelInx = QLabel(displayString, self)
		labelInx.setAlignment(Qt.AlignmentFlag.AlignCenter)
		h_layout.addWidget(labelInx)
		####

		#### name dir textview
		labelIn = QLineEdit(self.input)
		labelIn.textEdited.connect(self.textNameChanged)
		labelIn.setAlignment(Qt.AlignmentFlag.AlignCenter)
		if( validator ):
			labelIn.setValidator(validator)
		h_layout.addWidget(labelIn)
		####
	
	def textNameChanged(self, text):
		self.input = text
		print(self.input)
	
	def getText(self) -> str:
		return self.input


class LabelEditTextGroup(QWidget):
	def __init__(self) -> None:
		super().__init__()
		#### V-box for column
		self.vBoxLayout0 = QVBoxLayout(self)

	def add(self, labelEditText : LabelEditText) -> None :
		self.vBoxLayout0.addWidget(labelEditText)

	def clearAll(self):
		while self.vBoxLayout0.count():
			child = self.vBoxLayout0.takeAt(0)
			if child.widget():
				child.widget().deleteLater()
	
	# returns the value present in LabelEditTextGroup as a key pair map
	def getValues(self):
		ret = dict()		
		for i in range(self.vBoxLayout0.count()):
			w = self.vBoxLayout0.itemAt(i).widget()
			ret[w.displayString] = w.getText()
		
		return ret 
