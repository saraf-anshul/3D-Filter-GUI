
from PyQt6.QtWidgets import (
	QMainWindow, 
	QWidget, 
	QPushButton, 
	QFileDialog, 
	QLabel, 
	QVBoxLayout, 
	QHBoxLayout, 
	QGroupBox,
	QCheckBox,
)
from PIL import Image, ImageOps
from StorageUtils import *
from PyQt6.QtCore import pyqtSlot ,Qt
from LabelEditText import LabelEditText, LabelEditTextGroup
from FileInfoAndSelectorBox import FileInfoAndSelectorBox

from FilterUtils import getResourceMap


class MainWidget(QMainWindow):

	saveLocation = ""

	def __init__(self):
		super().__init__()
		
		### window attrs
		self.setWindowTitle("Filter Resource GUI")
		self.resize(750, 300)
		wid = QWidget(self)
		self.setCentralWidget(wid)
		layout = QVBoxLayout()
		wid.setLayout(layout)
		###
		
		### variables
		self.customResourceData = getResourceMap()
		###

		### sticker name label
		self.inputTB = LabelEditText("Filter name:  ")
		layout.addWidget(self.inputTB)
		###

		### sticker name label
		self.inputTB_V = LabelEditText("Filter version:")
		layout.addWidget(self.inputTB_V)
		###

		### flip - chceck
		self.inputCBFlip = QCheckBox("Filp")
		self.inputCBFlip.setChecked( False )
		self.inputCBFlip.setStyleSheet("QCheckBox {padding : 10px;}")
		layout.addWidget( self.inputCBFlip )
		###

		### button select
		self.stickerFileIn = FileInfoAndSelectorBox("Filter", "png", 1)
		layout.addWidget(self.stickerFileIn)
		###

		### resource info panel
		self.labelETGroup = LabelEditTextGroup()
		for i in range(len(self.customResourceData["Assets"])):
			self.labelETGroup.add(LabelEditText( self.customResourceData["Assets"][i]["Name"], None, self.customResourceData["Assets"][i]["Url"] ))
		layout.addWidget(self.labelETGroup)
		###

		### out-file dir select
		self.outputDir = QPushButton('Select output dir', self)
		self.outputDir.clicked.connect(self.on_click_dir)
		layout.addWidget(self.outputDir)
		###

		### horizontal layout (Output)
		horizontalGroupBox = QGroupBox()
		h_layout = QHBoxLayout()

		#### textview says "outupt Dir"
		self.labelOutx = QLabel('', self)
		self.labelOutx.setText("Output directory:")
		self.labelOutx.setAlignment(Qt.AlignmentFlag.AlignCenter)
		h_layout.addWidget(self.labelOutx)
		####

		#### out-file dir textview
		self.labelOut = QLabel('This is label', self)
		self.labelOut.setText("No output directory selected")
		self.labelOut.setAlignment(Qt.AlignmentFlag.AlignCenter)
		h_layout.addWidget(self.labelOut)
		####

		horizontalGroupBox.setLayout(h_layout)
		layout.addWidget(horizontalGroupBox)
		###

		### load save file or create
		try:
			with open( getLocationsFile() ,'r' ) as F:
				self.updateSaveLocation( json.load(F)['last'] )
		except:
			with open( getLocationsFile() ,'w' ) as F:
				json.dump({'last' : getDefaultStorageLocation()} ,F)
			self.updateSaveLocation( getDefaultStorageLocation() )
		###

		### run button
		self.button_run = QPushButton('Create', self)
		self.button_run.setToolTip('Run Script')
		self.button_run.setStyleSheet("QPushButton {background-color:#48A14D; border-radius: 4px; min-height: 22px;}")
		self.button_run.clicked.connect(self.run_script)
		layout.addWidget(self.button_run)
		###

	# download location onClick
	@pyqtSlot()
	def on_click_dir(self):
		dir = self.saveLocation

		dirName = QFileDialog().getExistingDirectory(self, 'Select an directory to save files' ,dir)
		if dirName:
			print(dirName)
			self.updateSaveLocation(dirName)

	@pyqtSlot()
	def run_script(self):
		oDir = self.saveLocation
		selectedFiles = self.stickerFileIn.selectedFiles
		if( len(selectedFiles) == 0 ):
			print( "no files selected" )
			return
		
		with open( getLocationsFile() ,'w' ) as F:
			json.dump({'last' : oDir} ,F)

		iDir = selectedFiles[0]
		if(self.inputCBFlip.isChecked()):
			imageObject = Image.open(iDir)
			imageObject_Flip = ImageOps.flip(imageObject)
			new_iDir = "".join(iDir.split(".")[:-1]) + "_flipped." + iDir.split(".")[-1]
			print(iDir, new_iDir)
			imageObject_Flip.save(new_iDir, quality=100)
			iDir = new_iDir

		name = self.inputTB.getText()
		v = self.inputTB_V.getText()
		editResourceData = self.labelETGroup.getValues()
		for i in range(len(self.customResourceData["Assets"])):
			assetName = self.customResourceData["Assets"][i]["Name"]
			self.customResourceData["Assets"][i]["Url"] = editResourceData[assetName]
		
		print(mapToJsonString(self.customResourceData))
		
		transformAndSave(name, v, iDir, oDir, mapToJsonString(self.customResourceData))

	def updateSaveLocation(self, loc):
		self.labelOut.setText(loc)
		self.saveLocation = loc

