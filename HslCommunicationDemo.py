'''
MIT License

Copyright (c) 2017-2020 Richard.Hu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
'''
警告：以下代码只能在测试PLC中运行，禁止使用生产现场的PLC来测试，否则，后果自负
Warning: The following code can only be run in the Test plc, prohibit the use of the production site PLC to test, otherwise, the consequences
'''

# 首先安装 HslCommunication，使用pip来安装 pip install HslCommunication

# 如何配置，然后让本界面的代码运行起来，需要参考如下的网址：https://www.cnblogs.com/dathlin/p/12142663.html
# 我想要PythonQt来做一个类似winform的demo软件

# how to configure, and then let the interface code to run, need to refer to the following url: https://www.cnblogs.com/dathlin/p/12142663.html
# I want PythonQt to do a winform demo

import datetime
import sys
import threading
import HslCommunication
from HslCommunication import SoftBasic, MelsecMcNet, MelsecMcAsciiNet, MelsecA1ENet, SiemensS7Net, SiemensPLCS, SiemensFetchWriteNet, OmronFinsNet, ModbusTcpNet, OperateResult, NetSimplifyClient

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication, QMessageBox, QAction, QPushButton, QVBoxLayout, QLineEdit, QTextEdit
from PyQt5.QtGui import QPalette, QFont, QIcon, QBrush, QColor, QPainter

class WindowsLoad(QtWidgets.QMainWindow):
	Language = 1                                 # 1代表中文，2代表英文
	ShowAuthorInfomation = True                  # 是否显示相关的信息
	WindowWidth = 1005
	WindowHeight = 645
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.setGeometry(100, 100, 1175, 700)                                           # 设置窗体的位置和大小情况
		self.setWindowTitle('HslCommunication Test Tool')                               # 设置窗体的标题
		self.center()
		self.setWindowIcon(QIcon('bitbug_favicon.ico'))
		self.setStyleSheet('WindowsLoad{background:#F0F8FF;font:微软雅黑;}')                # 设置背景
		# self.setFont(QtGui.QFont("微软雅黑"))

		self.menuBar = self.menuBar()                                                       # 创建一个菜单栏
		self.menuBar.setStyleSheet('QMenuBar{background:#404040;color:#cccccc}')            # 设置背景

		self.aboutMenu = self.menuBar.addMenu('About')                             # 添加About菜单

		self.blogAction = QAction('Blogs [博客]', self)
		self.blogAction.triggered.connect(self.blogClick)
		self.aboutMenu.addAction(self.blogAction)

		self.websiteAction = QAction( 'Website [官网]', self )
		self.websiteAction.triggered.connect(self.WebsiteClick)
		self.aboutMenu.addAction(self.websiteAction)

		self.mesDemoAction = QAction( 'Mes Demo [简易的MES演示]', self  )
		self.mesDemoAction.triggered.connect(self.MesDemoClick)
		self.aboutMenu.addAction(self.mesDemoAction)

		self.chineseAction = QAction( '简体中文', self )
		self.chineseAction.triggered.connect( self.ChineseClick )
		self.menuBar.addAction(self.chineseAction)

		self.englishAction = QAction( 'English', self )
		self.englishAction.triggered.connect( self.EnglishClick )
		self.menuBar.addAction(self.englishAction)

		self.bbsAction = QAction( '论坛', self )
		self.bbsAction.triggered.connect( self.BbsClick )
		self.menuBar.addAction(self.bbsAction)

		self.changeLogAction = QAction( '更新日志', self )
		self.changeLogAction.triggered.connect( self.changeLogClick )
		self.menuBar.addAction(self.changeLogAction)

		self.versionAction = QAction( 'Version: 1.0.0', self )
		self.menuBar.addAction(self.versionAction)

		# 三菱的PLC的数据通信
		self.melsecGroupBox = QtWidgets.QGroupBox(self)
		self.melsecGroupBox.setTitle("Melsec PLC(三菱)")
		self.melsecGroupBox.setGeometry(QtCore.QRect(9, 29, 183, 335))
		self.pushButton1 = QtWidgets.QPushButton(self.melsecGroupBox)
		self.pushButton1.setGeometry(QtCore.QRect(15, 24, 150, 32))
		self.pushButton1.setText("MC (Binary)")
		self.pushButton1.clicked.connect(self.pushButton1_Click)
		self.pushButton1.setObjectName("pushButton1")

		self.pushButton2 = QtWidgets.QPushButton(self.melsecGroupBox)
		self.pushButton2.setGeometry(QtCore.QRect(15, 64, 150, 32))
		self.pushButton2.setText("MC (ASCII)")
		self.pushButton2.setObjectName("pushButton2")
		self.pushButton2.clicked.connect(self.pushButton2_Click)

		self.pushButton3 = QtWidgets.QPushButton(self.melsecGroupBox)
		self.pushButton3.setGeometry(QtCore.QRect(15, 104, 150, 32))
		self.pushButton3.setText("A-1E (Binary)")
		self.pushButton3.setObjectName("pushButton3")
		self.pushButton3.clicked.connect(self.pushButton3_Click)

		# 西门子的PLC的数据通信
		self.siemensGroupBox = QtWidgets.QGroupBox(self)
		self.siemensGroupBox.setTitle("Siemens PLC(西门子)")
		self.siemensGroupBox.setGeometry(QtCore.QRect(203, 29, 183, 335))
		self.pushButton101 = QtWidgets.QPushButton(self.siemensGroupBox)
		self.pushButton101.setGeometry(QtCore.QRect(18, 24, 150, 32))
		self.pushButton101.setText("S7-1200")
		self.pushButton101.setObjectName("pushButton101")
		self.pushButton101.clicked.connect(self.pushButton101_Click)

		self.pushButton102 = QtWidgets.QPushButton(self.siemensGroupBox)
		self.pushButton102.setGeometry(QtCore.QRect(18, 64, 150, 32))
		self.pushButton102.setText("S7-1500")
		self.pushButton102.setObjectName("pushButton102")
		self.pushButton102.clicked.connect(self.pushButton102_click)
		
		self.pushButton103 = QtWidgets.QPushButton(self.siemensGroupBox)
		self.pushButton103.setGeometry(QtCore.QRect(18, 104, 150, 32))
		self.pushButton103.setText("S7-400")
		self.pushButton103.setObjectName("pushButton103")
		self.pushButton103.clicked.connect(self.pushButton103_click)

		self.pushButton104 = QtWidgets.QPushButton(self.siemensGroupBox)
		self.pushButton104.setGeometry(QtCore.QRect(18, 144, 150, 32))
		self.pushButton104.setText("S7-300")
		self.pushButton104.setObjectName("pushButton104")
		self.pushButton104.clicked.connect(self.pushButton104_click)

		self.pushButton105 = QtWidgets.QPushButton(self.siemensGroupBox)
		self.pushButton105.setGeometry(QtCore.QRect(18, 184, 150, 32))
		self.pushButton105.setText("s7-200")
		self.pushButton105.setObjectName("pushButton105")
		self.pushButton105.setEnabled(False)

		self.pushButton106 = QtWidgets.QPushButton(self.siemensGroupBox)
		self.pushButton106.setGeometry(QtCore.QRect(18, 224, 150, 32))
		self.pushButton106.setText("s7-200Smart")
		self.pushButton106.setObjectName("pushButton106")
		self.pushButton106.clicked.connect(self.pushButton106_click)

		self.pushButton107 = QtWidgets.QPushButton(self.siemensGroupBox)
		self.pushButton107.setGeometry(QtCore.QRect(18, 264, 150, 32))
		self.pushButton107.setText("Fetch/Write")
		self.pushButton107.setObjectName("pushButton107")
		self.pushButton107.clicked.connect(self.pushButton107_click)

		# Modbus
		self.modbusGroupBox = QtWidgets.QGroupBox(self)
		self.modbusGroupBox.setTitle("Modbus")
		self.modbusGroupBox.setGeometry(QtCore.QRect(395, 29, 185, 335))
		self.pushButton201 = QtWidgets.QPushButton(self.modbusGroupBox)
		self.pushButton201.setGeometry(QtCore.QRect(15, 24, 150, 32))
		self.pushButton201.setText("Modbus Tcp")
		self.pushButton201.setObjectName("pushButton201")
		self.pushButton201.clicked.connect(self.pushButton201_click)

		# Omron
		self.omronGroupBox = QtWidgets.QGroupBox(self)
		self.omronGroupBox.setTitle("Omron PLC(欧姆龙)")
		self.omronGroupBox.setGeometry(QtCore.QRect(586, 29, 185, 187))
		self.pushButton301 = QtWidgets.QPushButton(self.omronGroupBox)
		self.pushButton301.setGeometry(QtCore.QRect(15, 24, 150, 32))
		self.pushButton301.setText("Fins Tcp")
		self.pushButton301.setObjectName("pushButton301")
		self.pushButton301.clicked.connect(self.pushButton301_click)

		# Lsis
		self.lsisGroupBox = QtWidgets.QGroupBox(self)
		self.lsisGroupBox.setTitle("Lsis PLC")
		self.lsisGroupBox.setGeometry(QtCore.QRect(586, 224, 185, 140))

		# Panasonic
		self.panasonicGroupBox = QtWidgets.QGroupBox(self)
		self.panasonicGroupBox.setTitle("Panasonic PLC(松下)")
		self.panasonicGroupBox.setGeometry(QtCore.QRect(777, 29, 185, 187))

		# Keyence
		self.keyenceGroupBox = QtWidgets.QGroupBox(self)
		self.keyenceGroupBox.setTitle("Keyence PLC(基恩士)")
		self.keyenceGroupBox.setGeometry(QtCore.QRect(777, 224, 185, 140))

		# FATEK
		self.fatekGroupBox = QtWidgets.QGroupBox(self)
		self.fatekGroupBox.setTitle("FATEK PLC(永宏)")
		self.fatekGroupBox.setGeometry(QtCore.QRect(968, 29, 185, 96))

		# AllenBradly
		self.abGroupBox = QtWidgets.QGroupBox(self)
		self.abGroupBox.setTitle("AB PLC(罗克韦尔)")
		self.abGroupBox.setGeometry(QtCore.QRect(968, 133, 185, 121))

		# Fuji
		self.fujiGroupBox = QtWidgets.QGroupBox(self)
		self.fujiGroupBox.setTitle("Fuji PLC(富士)")
		self.fujiGroupBox.setGeometry(QtCore.QRect(968, 262, 185, 102))

		# HSL
		self.fujiGroupBox = QtWidgets.QGroupBox(self)
		self.fujiGroupBox.setTitle("Hsl Support(HSL协议)")
		self.fujiGroupBox.setGeometry(QtCore.QRect(9, 372, 183, 315))

		#self.melsecLayout.setGeometry( 9, 29, 183, 335)
		#self.melsecLayout.setStyleSheet('QVBoxLayout{border:1px solid gray;border-radius:10px;padding:2px 4px;}')                # 设置背景
		self.setFont(QFont("微软雅黑", 15))
		t1 = threading.Thread(target=self.threadReadFromServer, args=(13,))
		t1.start()

	def threadReadFromServer(self, num):
		netSimplifyClient = NetSimplifyClient('118.24.36.220', 18467)
		# netSimplifyClient.Token = uuid.UUID('66a469ad-a595-48ed-abe1-912f7085dbcd')
		# netSimplifyClient.SetLoginAccount("admin","123456")  # 如果采用了账户名和密码的验证，就使用这个方法
		connect = netSimplifyClient.ConnectServer()
		if connect.IsSuccess == False:
			print(connect.Message)
		else:
			netSimplifyClient.ReadFromServer(600,'1.0.0')
			netSimplifyClient.ConnectClose()

	#控制窗口显示在屏幕中心的方法
	def center(self):
		#获得窗口
		qr = self.frameGeometry()
		#获得屏幕中心点
		cp = QDesktopWidget().availableGeometry().center()
		#显示到屏幕中心
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	def blogClick( self ):
		QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://www.cnblogs.com/dathlin/'))
	def WebsiteClick( self ):
		QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://118.24.36.220/'))
	def MesDemoClick( self ):
		QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://118.24.36.220/'))
	def ChineseClick( self ):
		HslCommunication.StringResources.Language = HslCommunication.DefaultLanguage()
		QMessageBox.information(self,'Info','当前已经选择中文')
		WindowsLoad.Language = 1
		self.bbsAction.setText('论坛')
		self.changeLogAction.setText('更新日志')
	def EnglishClick( self ):
		HslCommunication.StringResources.Language = HslCommunication.English()
		QMessageBox.information(self,'Info','English Selected !')
		WindowsLoad.Language = 2
		self.bbsAction.setText('Bbs')
		self.changeLogAction.setText('Change Log')
	def BbsClick( self ):
		QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://118.24.36.220/'))
	def changeLogClick( self ):
		QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://118.24.36.220:8080/'))
	def AboutClick( self ):
		reply = QMessageBox.question(self,'询问','这是一个询问消息对话框，默认是No', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.No)
	def pushButton1_Click(self):
		self.formMelsecBinary = FormMelsecBinary()
		self.formMelsecBinary.show()
	def pushButton2_Click(self):
		self.formMelsecAscii = FormMelsecAscii()
		self.formMelsecAscii.show()
	def pushButton3_Click(self):
		self.formMelsecA1E = FormMelsecA1E()
		self.formMelsecA1E.show()
	def pushButton101_Click(self):
		self.formSiemens = FormSiemens(SiemensPLCS.S1200)
		self.formSiemens.show()
	def pushButton102_click(self):
		self.formSiemens = FormSiemens(SiemensPLCS.S1500)
		self.formSiemens.show()
	def pushButton103_click(self):
		self.formSiemens = FormSiemens(SiemensPLCS.S400)
		self.formSiemens.show()
	def pushButton104_click(self):
		self.formSiemens = FormSiemens(SiemensPLCS.S300)
		self.formSiemens.show()
	def pushButton105_click(self):
		self.formSiemens = FormSiemens(SiemensPLCS.S1200)
		self.formSiemens.show()
	def pushButton106_click(self):
		self.formSiemens = FormSiemens(SiemensPLCS.S200Smart)
		self.formSiemens.show()
	def pushButton107_click(self):
		self.formFW = FormSiemensFetchWriteNet()
		self.formFW.show()

	def pushButton201_click(self):
		self.modbus = FormModbus()
		self.modbus.show()

	def pushButton301_click(self):
		self.omron = FormOmron()
		self.omron.show()

	def show(self):
		super().show()

class DemoUtils:
	@staticmethod
	def ReadResultRender(result : OperateResult, address : str, textBox : QTextEdit):
		if result.IsSuccess == True:
			if result.Content is list:
				textBox.append(datetime.datetime.now().strftime('%H:%M:%S') + " [" + address  + "] "+ SoftBasic.ArrayFormat(result.Content))
			else:
				textBox.append(datetime.datetime.now().strftime('%H:%M:%S') + " [" + address  + "] "+ str(result.Content))
		else:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + address + " Read Failed\nReason:"+ result.ToMessageShowString())
	@staticmethod
	def WriteResultRender(result : OperateResult, address : str):
		if result.IsSuccess:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + address + " Write Success")
		else:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + address + " Write Failed\nReason:"+ result.ToMessageShowString())
class UserControlHead(QWidget):
	def __init__(self, parent = None):
		super().__init__()
		self.setParent(parent)
		self.initUI()
	def initUI(self):
		self.setMinimumSize(800, 32)
		self.HelpLink = 'http://www.hslcommunication.cn/'

		self.helpLinkLabel1 = QtWidgets.QLabel('博客地址：', self)
		self.helpLinkLabel1.move(13, 10)

		self.helpLinkLabel = QtWidgets.QLabel(self.HelpLink, self)
		self.helpLinkLabel.move(80, 10)
		self.helpLinkLabel.mousePressEvent = self.pushButtonClick

		self.protocol1 = QtWidgets.QLabel('使用协议：', self)
		self.protocol1.move(544, 10)

		self.protocol = QtWidgets.QLabel('HSL', self)
		self.protocol.move(618, 10)

		self.version = QtWidgets.QLabel('Version: ', self)
		self.version.move(886, 10)

		self.setStyleSheet('QWidget{color:#eeeeee;}')
	def paintEvent(self, e):
		qp = QPainter()
		qp.begin(self)
		self.drawWidget(qp)
		qp.end()
	def drawWidget(self, qp):
		qp.setBrush(QColor(0x40, 0x40, 0x40))
		qp.drawRect(0, 0, self.size().width(), self.size().height())
	def pushButtonClick(self, e):
		QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.helpLinkLabel.text()))
	def setHelpLink( self, value : str ):
		'''设置显示的帮助链接'''
		self.HelpLink = value
		self.helpLinkLabel.setText(value)
	def setProtocol( self, value : str ):
		'''设置协议名称'''
		self.protocol.setText(value)

class UserControlReadWriteOp(QWidget):
	def __init__(self, parent = None):
		super().__init__()
		self.setParent(parent)
		self.initUI()
	def initUI(self):
		self.setMinimumSize(954, 240)
		self.setBaseSize(954, 240)

		# 读取的控件信息
		self.readGroupBox = QtWidgets.QGroupBox(self)
		self.readGroupBox.setTitle('Read Data Single')
		self.readGroupBox.setGeometry(0, 0, 518, 234)
		self.label1 = QtWidgets.QLabel('Address:', self.readGroupBox)
		self.label1.move(9, 30)
		self.textbox3 = QtWidgets.QLineEdit('', self.readGroupBox)
		self.textbox3.setGeometry(63, 27, 185, 24)
		self.textbox5 = QtWidgets.QLineEdit('', self.readGroupBox)
		self.textbox5.setGeometry(254, 27, 42, 24)
		self.textbox5.setText('1')
		self.label7 = QtWidgets.QLabel("Result:", self.readGroupBox)
		self.label7.move(9, 58)
		self.textbox4 = QtWidgets.QTextEdit("", self.readGroupBox)
		self.textbox4.setGeometry(63, 56, 233, 164)

		self.button_read_bool = QtWidgets.QPushButton('r-bool', self.readGroupBox)
		self.button_read_bool.setGeometry(315, 19, 82, 28)
		self.button_read_byte = QtWidgets.QPushButton('r-byte', self.readGroupBox)
		self.button_read_byte.setGeometry(415, 19, 82, 28)
		self.button_read_short = QtWidgets.QPushButton('r-short', self.readGroupBox)
		self.button_read_short.setGeometry(315, 56, 82, 28)
		self.button_read_ushort = QtWidgets.QPushButton('r-ushort', self.readGroupBox)
		self.button_read_ushort.setGeometry(415, 56, 82, 28)
		self.button_read_int = QtWidgets.QPushButton('r-int', self.readGroupBox)
		self.button_read_int.setGeometry(315, 90, 82, 28)
		self.button_read_uint = QtWidgets.QPushButton('r-uint', self.readGroupBox)
		self.button_read_uint.setGeometry(415, 90, 82, 28)
		self.button_read_long = QtWidgets.QPushButton('r-long', self.readGroupBox)
		self.button_read_long.setGeometry(315, 124, 82, 28)
		self.button_read_ulong = QtWidgets.QPushButton('r-ulong', self.readGroupBox)
		self.button_read_ulong.setGeometry(415, 124, 82, 28)
		self.button_read_float = QtWidgets.QPushButton('r-float', self.readGroupBox)
		self.button_read_float.setGeometry(315, 158, 82, 28)
		self.button_read_double = QtWidgets.QPushButton('r-double', self.readGroupBox)
		self.button_read_double.setGeometry(415, 158, 82, 28)
		self.label8 = QtWidgets.QLabel("Length:", self.readGroupBox)
		self.label8.move(312, 198)
		self.textbox1 = QtWidgets.QLineEdit("", self.readGroupBox)
		self.textbox1.setGeometry(365, 195, 41, 24)
		self.button_read_string = QtWidgets.QPushButton('r-string', self.readGroupBox)
		self.button_read_string.setGeometry(415, 195, 82, 28)
		# 写入的控件信息
		self.writeGroupBox = QtWidgets.QGroupBox(self)
		self.writeGroupBox.setTitle('Write Data Single')
		self.writeGroupBox.setGeometry(535, 0, 419, 234)
		self.label10 = QtWidgets.QLabel('Address:', self.writeGroupBox)
		self.label10.move(9, 30)
		self.textbox8 = QtWidgets.QLineEdit('', self.writeGroupBox)
		self.textbox8.setGeometry(63, 27, 132, 24)
		self.label9 = QtWidgets.QLabel('Address:', self.writeGroupBox)
		self.label9.move(9, 30)
		self.textbox7 = QtWidgets.QLineEdit('', self.writeGroupBox)
		self.textbox7.setGeometry(63, 56, 132, 24)
		self.textbox7.setText('False')
		self.button_write_bool = QtWidgets.QPushButton('w-bool', self.writeGroupBox)
		self.button_write_bool.setGeometry(226, 19, 82, 28)
		self.button_write_byte = QtWidgets.QPushButton('w-byte', self.writeGroupBox)
		self.button_write_byte.setGeometry(326, 19, 82, 28)
		self.button_write_short = QtWidgets.QPushButton('w-short', self.writeGroupBox)
		self.button_write_short.setGeometry(226, 56, 82, 28)
		self.button_write_ushort = QtWidgets.QPushButton('w-ushort', self.writeGroupBox)
		self.button_write_ushort.setGeometry(326, 56, 82, 28)
		self.button_write_int = QtWidgets.QPushButton('w-int', self.writeGroupBox)
		self.button_write_int.setGeometry(226, 90, 82, 28)
		self.button_write_uint = QtWidgets.QPushButton('w-uint', self.writeGroupBox)
		self.button_write_uint.setGeometry(326, 90, 82, 28)
		self.button_write_long = QtWidgets.QPushButton('w-long', self.writeGroupBox)
		self.button_write_long.setGeometry(226, 124, 82, 28)
		self.button_write_ulong = QtWidgets.QPushButton('w-ulong', self.writeGroupBox)
		self.button_write_ulong.setGeometry(326, 124, 82, 28)
		self.button_write_float = QtWidgets.QPushButton('w-float', self.writeGroupBox)
		self.button_write_float.setGeometry(226, 158, 82, 28)
		self.button_write_double = QtWidgets.QPushButton('w-double', self.writeGroupBox)
		self.button_write_double.setGeometry(326, 158, 82, 28)
		self.button_write_string = QtWidgets.QPushButton('w-string', self.writeGroupBox)
		self.button_write_string.setGeometry(326, 195, 82, 28)
		self.label19 = QtWidgets.QLabel('Note: The value of the string needs to be converted', self.writeGroupBox)
		self.label19.setGeometry(61, 82, 147, 58)
		self.label19.setWordWrap(True)
		self.label19.setStyleSheet('color:#ff0000')

		self.readWriteNet = None
		self.button_read_bool.clicked.connect(self.button_read_bool_click)
		self.button_read_byte.clicked.connect(self.button_read_byte_click)
		self.button_read_short.clicked.connect(self.button_read_short_click)
		self.button_read_ushort.clicked.connect(self.button_read_ushort_click)
		self.button_read_int.clicked.connect(self.button_read_int_click)
		self.button_read_uint.clicked.connect(self.button_read_uint_click)
		self.button_read_long.clicked.connect(self.button_read_long_click)
		self.button_read_ulong.clicked.connect(self.button_read_ulong_click)
		self.button_read_float.clicked.connect(self.button_read_float_click)
		self.button_read_double.clicked.connect(self.button_read_double_click)
		self.button_read_string.clicked.connect(self.button_read_string_click)
		self.button_write_bool.clicked.connect(self.button_write_bool_click)
		self.button_write_byte.clicked.connect(self.button_write_byte_click)
		self.button_write_short.clicked.connect(self.button_write_short_click)
		self.button_write_ushort.clicked.connect(self.button_write_ushort_click)
		self.button_write_int.clicked.connect(self.button_write_int_click)
		self.button_write_uint.clicked.connect(self.button_write_uint_click)
		self.button_write_long.clicked.connect(self.button_write_long_click)
		self.button_write_ulong.clicked.connect(self.button_write_ulong_click)
		self.button_write_float.clicked.connect(self.button_write_float_click)
		self.button_write_double.clicked.connect(self.button_write_double_click)
		self.button_write_string.clicked.connect(self.button_write_string_click)

	def button_read_bool_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadBool(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadBool(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_byte_click(self):
		DemoUtils.ReadResultRender(self.readWriteNet.ReadByte(self.textbox3.text()), self.textbox3.text(), self.textbox4)
	def button_read_short_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadInt16(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadInt16(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_ushort_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadUInt16(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadUInt16(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_int_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadInt32(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadInt32(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_uint_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadUInt32(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadUInt32(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_long_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadInt64(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadInt64(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_ulong_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadUInt64(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadUInt64(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_float_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadFloat(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadFloat(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_double_click(self):
		if self.textbox5.text() == "1":
			DemoUtils.ReadResultRender(self.readWriteNet.ReadDouble(self.textbox3.text()), self.textbox3.text(), self.textbox4)
		else:
			DemoUtils.ReadResultRender(self.readWriteNet.ReadDouble(self.textbox3.text(), int(self.textbox5.text())), self.textbox3.text(), self.textbox4)
	def button_read_string_click(self):
		DemoUtils.ReadResultRender(self.readWriteNet.ReadString(self.textbox3.text(),  int(self.textbox1.text())), self.textbox3.text(), self.textbox4)
	# 写入部分的内容
	def button_write_bool_click(self):
		if self.textbox7.text().lower() == "true":
			DemoUtils.WriteResultRender(self.readWriteNet.WriteBool(self.textbox8.text(), True), self.textbox8.text())
		else:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteBool(self.textbox8.text(), False), self.textbox8.text())
	def button_write_byte_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteByte(self.textbox8.text(), int(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_short_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteInt16(self.textbox8.text(), int(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_ushort_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteUInt16(self.textbox8.text(), int(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_int_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteInt32(self.textbox8.text(), int(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_uint_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteUInt32(self.textbox8.text(), int(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_long_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteInt64(self.textbox8.text(), int(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_ulong_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteUInt64(self.textbox8.text(), int(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_float_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteFloat(self.textbox8.text(), float(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_double_click(self):
		try:
			DemoUtils.WriteResultRender(self.readWriteNet.WriteDouble(self.textbox8.text(), float(self.textbox7.text())), self.textbox8.text())
		except Exception as ex:
			QMessageBox.information(None,'Info',datetime.datetime.now().strftime('%H:%M:%S')  + self.textbox8.text() + " Write Failed: " + str(ex))
	def button_write_string_click(self):
		DemoUtils.WriteResultRender(self.readWriteNet.WriteString(self.textbox8.text(), self.textbox7.text()), self.textbox8.text())

	def SetReadWriteNet( self, readWrite, address, strLength = 10 ):
		self.address = address
		self.textbox3.setText(self.address)
		self.textbox8.setText(self.address)
		self.textbox1.setText(str(strLength))
		self.readWriteNet = readWrite
		try:
			if self.readWriteNet.ReadByte == None:
				self.button_read_byte.setEnabled(False)
		except:
			self.button_read_byte.setEnabled(False)
		try:
			if self.readWriteNet.WriteByte == None:
				self.button_write_byte.setEnabled(False)
		except:
			self.button_write_byte.setEnabled(False)


class FormMelsecBinary(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.setGeometry(100, 100, WindowsLoad.WindowWidth, WindowsLoad.WindowHeight)                                 # 设置窗体的位置和大小情况
		self.setWindowTitle('三菱PLC访问Demo')                                # 设置窗体的标题
		self.userControlHead = UserControlHead(self)
		self.userControlHead.setGeometry(QtCore.QRect(0, 0, 1004, 32))
		self.userControlHead.protocol.setText('MC 3E Binary')
		
		self.melsec = None
		self.Address = 'D100'

		self.settings = QtWidgets.QWidget(self)
		self.settings.setGeometry(QtCore.QRect(14, 44, 978, 42))
		self.settings.setObjectName('settings')
		self.settings.setStyleSheet('QWidget#settings{border:1px solid gray;}')
		self.setStyleSheet('FormMelsecBinary{background:#F0F8FF;font:微软雅黑;}')
		self.label1 = QtWidgets.QLabel('Ip：', self.settings)
		self.label1.move(10, 12)
		self.textboxIp = QtWidgets.QLineEdit("", self.settings)
		self.textboxIp.setGeometry(50, 8, 100, 24)
		self.textboxIp.setText('192.168.8.14')
		self.label2 = QtWidgets.QLabel('Port：', self.settings)
		self.label2.move(180, 12)
		self.textboxPort = QtWidgets.QLineEdit("", self.settings)
		self.textboxPort.setGeometry(220, 8, 50, 24)
		self.textboxPort.setText('6000')
		self.buttonConnect = QtWidgets.QPushButton('Connect', self.settings)
		self.buttonConnect.setGeometry(300, 8, 100, 24)
		self.buttonConnect.clicked.connect(self.button_connect_click)
		self.buttonDisConnect = QtWidgets.QPushButton('DisConnect', self.settings)
		self.buttonDisConnect.setGeometry(450, 8, 100, 24)
		self.buttonDisConnect.clicked.connect(self.button_disconnect_click)
		self.buttonDisConnect.setEnabled(False)
		# panel2
		self.panel2 = QtWidgets.QWidget(self)
		self.panel2.setGeometry(14, 95, 978, 537)
		self.panel2.setObjectName('panel2')
		self.panel2.setStyleSheet('QWidget#panel2{border:1px solid gray;}')
		self.userControlReadWriteOp1 = UserControlReadWriteOp(self.panel2)
		self.userControlReadWriteOp1.move(11, 2)
		# groupBox3
		self.groupBox3 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox3.setTitle('Bulk Read test')
		self.groupBox3.setGeometry(11, 243, 518, 154)
		self.label11 = QtWidgets.QLabel('Address：', self.groupBox3)
		self.label11.move(9, 30)
		self.textbox6 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox6.setGeometry(63, 27, 116, 23)
		self.textbox6.setText(self.Address)
		self.label12 = QtWidgets.QLabel('Length：', self.groupBox3)
		self.label12.move(182, 30)
		self.textbox9 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox9.setGeometry(222, 27, 49, 23)
		self.textbox9.setText('10')
		self.button9 = QtWidgets.QPushButton('r-Random', self.groupBox3)
		self.button9.setGeometry(277, 24, 77, 28)
		self.button9.setEnabled(False)
		self.button6 = QtWidgets.QPushButton('plc-type', self.groupBox3)
		self.button6.setGeometry(360, 24, 72, 28)
		self.button6.setEnabled(False)
		self.button25 = QtWidgets.QPushButton('bulk read', self.groupBox3)
		self.button25.setGeometry(436, 24, 72, 28)
		self.button25.clicked.connect(self.button25_click)
		self.label13 = QtWidgets.QLabel("Result:", self.groupBox3)
		self.label13.move(9, 62)
		self.textbox10 = QtWidgets.QTextEdit("", self.groupBox3)
		self.textbox10.setGeometry(63, 60, 445, 78)
		# groupBox4
		self.groupBox4 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox4.setTitle('Message reading test, hex string needs to be filled in')
		self.groupBox4.setGeometry(11, 403, 518, 118)
		self.label16 = QtWidgets.QLabel('Message：', self.groupBox4)
		self.label16.move(9, 30)
		self.textbox13 = QtWidgets.QLineEdit('', self.groupBox4)
		self.textbox13.setGeometry(63, 27, 357, 23)
		self.button26 = QtWidgets.QPushButton('Read', self.groupBox4)
		self.button26.setGeometry(426, 24, 82, 28)
		self.button26.clicked.connect(self.button26_click)
		self.label14 = QtWidgets.QLabel("Result:", self.groupBox4)
		self.label14.move(9, 62)
		self.textbox11 = QtWidgets.QTextEdit('', self.groupBox4)
		self.textbox11.setGeometry(63, 60, 445, 52)
		# groupBox5
		self.groupBox5 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox5.setTitle('Special function test')
		self.groupBox5.setGeometry(546, 243, 419, 278)
		self.button7 = QtWidgets.QPushButton('remote reset', self.groupBox5)
		self.button7.setGeometry(16, 24, 92, 28)
		self.button7.clicked.connect(self.button7_click)
		self.button8 = QtWidgets.QPushButton('error reset', self.groupBox5)
		self.button8.setGeometry(114, 24, 92, 28)
		self.button8.clicked.connect(self.button8_click)
		self.button4 = QtWidgets.QPushButton('remote run', self.groupBox5)
		self.button4.setGeometry(212, 24, 86, 28)
		self.button4.clicked.connect(self.button4_click)
		self.button5 = QtWidgets.QPushButton('remote stop', self.groupBox5)
		self.button5.setGeometry(310, 24, 94, 28)
		self.button5.clicked.connect(self.button5_click)
		self.textbox3 = QtWidgets.QTextEdit('', self.groupBox5)
		self.textbox3.setGeometry(16, 93, 388, 145)

		self.panel2.setEnabled(False)
		self.center()
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2,
				  (screen.height() - size.height()) / 2)
	def button_connect_click(self):
		self.melsec = MelsecMcNet(self.textboxIp.text(), int(self.textboxPort.text()))
		connect = self.melsec.ConnectServer()
		if connect.IsSuccess == False:
			QMessageBox.information(self,'Info','Connect Failed: ' + connect.ToMessageShowString())
		else:
			QMessageBox.information(self,'Info','Connect Success!')
			self.buttonConnect.setEnabled(False)
			self.buttonDisConnect.setEnabled(True)
			self.panel2.setEnabled(True)
			self.userControlReadWriteOp1.SetReadWriteNet(self.melsec, self.Address)
	def button_disconnect_click(self):
		disconnect = self.melsec.ConnectClose()
		if disconnect.IsSuccess == True:
			self.panel2.setEnabled(False)
			self.buttonConnect.setEnabled(True)
			self.buttonDisConnect.setEnabled(False)
		else:
			QMessageBox.information(self,'Info','DisConnect Failed: ' + disconnect.ToMessageShowString())
	def button25_click(self):
		read = self.melsec.Read(self.textbox6.text(), int(self.textbox9.text()))
		if read.IsSuccess == True:
			self.textbox10.setText(datetime.datetime.now().strftime('%H:%M:%S') + " [" + self.textbox6.text()  + "] "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())
	def button26_click(self):
		read = self.melsec.ReadFromCoreServer(SoftBasic.HexStringToBytes(self.textbox13.text()))
		if read.IsSuccess == True:
			self.textbox11.setText(datetime.datetime.now().strftime('%H:%M:%S') + " "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())
	def button7_click(self):
		QMessageBox.information(self,'Info','It hasn\'t been implemented yet')
	def button8_click(self):
		QMessageBox.information(self,'Info','It hasn\'t been implemented yet')
	def button4_click(self):
		QMessageBox.information(self,'Info','It hasn\'t been implemented yet')
	def button5_click(self):
		QMessageBox.information(self,'Info','It hasn\'t been implemented yet')

class FormMelsecAscii(FormMelsecBinary):
	def __init__(self):
		super().__init__()
		self.userControlHead.protocol.setText('MC 3E ASCII')
	def button_connect_click(self):
		self.melsec = MelsecMcAsciiNet(self.textboxIp.text(), int(self.textboxPort.text()))
		connect = self.melsec.ConnectServer()
		if connect.IsSuccess == False:
			QMessageBox.information(self,'Info','Connect Failed: ' + connect.ToMessageShowString())
		else:
			QMessageBox.information(self,'Info','Connect Success!')
			self.buttonConnect.setEnabled(False)
			self.buttonDisConnect.setEnabled(True)
			self.panel2.setEnabled(True)
			self.userControlReadWriteOp1.SetReadWriteNet(self.melsec, self.Address)

class FormMelsecA1E(FormMelsecBinary):
	def __init__(self):
		super().__init__()
		self.userControlHead.protocol.setText('MC 1E Binary')
		self.button9.close()
		self.button6.close()
	def button_connect_click(self):
		self.melsec = MelsecA1ENet(self.textboxIp.text(), int(self.textboxPort.text()))
		connect = self.melsec.ConnectServer()
		if connect.IsSuccess == False:
			QMessageBox.information(self,'Info','Connect Failed: ' + connect.ToMessageShowString())
		else:
			QMessageBox.information(self,'Info','Connect Success!')
			self.buttonConnect.setEnabled(False)
			self.buttonDisConnect.setEnabled(True)
			self.panel2.setEnabled(True)
			self.userControlReadWriteOp1.SetReadWriteNet(self.melsec, self.Address)

class FormSiemens(QtWidgets.QMainWindow):
	def __init__(self, plc : SiemensPLCS):
		self.siemensPLCS = plc
		super().__init__()
		self.initUI()
	def initUI(self):
		self.setGeometry(100, 100, WindowsLoad.WindowWidth, WindowsLoad.WindowHeight)                                 # 设置窗体的位置和大小情况
		self.setWindowTitle('西门子PLC访问Demo')                                # 设置窗体的标题
		self.userControlHead = UserControlHead(self)
		self.userControlHead.setGeometry(QtCore.QRect(0, 0, 1004, 32))
		self.userControlHead.setProtocol('S7')
		
		self.siemens = None
		self.Address = 'M100'

		self.settings = QtWidgets.QWidget(self)
		self.settings.setGeometry(QtCore.QRect(14, 44, 978, 54))
		self.settings.setObjectName('settings')
		self.settings.setStyleSheet('QWidget#settings{border:1px solid gray;}')
		self.setStyleSheet('FormSiemens{background:#F0F8FF;font:微软雅黑;}')
		self.label1 = QtWidgets.QLabel('Ip：', self.settings)
		self.label1.move(10, 12)
		self.textboxIp = QtWidgets.QLineEdit("", self.settings)
		self.textboxIp.setGeometry(50, 8, 100, 24)
		self.textboxIp.setText('192.168.8.12')
		self.label2 = QtWidgets.QLabel('Port：', self.settings)
		self.label2.move(180, 12)
		self.textboxPort = QtWidgets.QLineEdit("", self.settings)
		self.textboxPort.setGeometry(220, 8, 50, 24)
		self.textboxPort.setText('102')
		self.label23= QtWidgets.QLabel('Rack:', self.settings)
		self.label23.move(305, 10)
		self.textbox15 = QtWidgets.QLineEdit('0', self.settings)
		self.textbox15.setGeometry(354, 7, 33, 23)
		self.label23= QtWidgets.QLabel('Slot:', self.settings)
		self.label23.move(393, 10)
		self.textbox16 = QtWidgets.QLineEdit('0', self.settings)
		self.textbox16.setGeometry(439, 7, 33, 23)
		self.label25= QtWidgets.QLabel('Not use for s7-200 smart', self.settings)
		self.label25.move(317, 33)
		self.buttonConnect = QtWidgets.QPushButton('Connect', self.settings)
		self.buttonConnect.setGeometry(496, 11, 91, 28)
		self.buttonConnect.clicked.connect(self.button_connect_click)
		self.buttonDisConnect = QtWidgets.QPushButton('DisConnect', self.settings)
		self.buttonDisConnect.setGeometry(593, 11, 91, 28)
		self.buttonDisConnect.clicked.connect(self.button_disconnect_click)
		self.buttonDisConnect.setEnabled(False)
		# panel2
		self.panel2 = QtWidgets.QWidget(self)
		self.panel2.setGeometry(14, 99, 978, 537)
		self.panel2.setObjectName('panel2')
		self.panel2.setStyleSheet('QWidget#panel2{border:1px solid gray;}')
		self.userControlReadWriteOp1 = UserControlReadWriteOp(self.panel2)
		self.userControlReadWriteOp1.move(11, 2)
		# groupBox3
		self.groupBox3 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox3.setTitle('Bulk Read test')
		self.groupBox3.setGeometry(11, 243, 518, 154)
		self.label11 = QtWidgets.QLabel('Address：', self.groupBox3)
		self.label11.move(9, 30)
		self.textbox6 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox6.setGeometry(63, 27, 102, 23)
		self.textbox6.setText(self.Address)
		self.label12 = QtWidgets.QLabel('Length：', self.groupBox3)
		self.label12.move(180, 30)
		self.textbox9 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox9.setGeometry(234, 27, 102, 23)
		self.textbox9.setText('10')
		self.button3 = QtWidgets.QPushButton('Order Number', self.groupBox3)
		self.button3.setGeometry(342, 24, 82, 28)
		self.button3.clicked.connect(self.button3_click)
		self.button25 = QtWidgets.QPushButton('bulk read', self.groupBox3)
		self.button25.setGeometry(426, 24, 82, 28)
		self.button25.clicked.connect(self.button25_click)
		self.label13 = QtWidgets.QLabel("Result:", self.groupBox3)
		self.label13.move(9, 62)
		self.textbox10 = QtWidgets.QTextEdit("", self.groupBox3)
		self.textbox10.setGeometry(63, 60, 445, 78)
		# groupBox4
		self.groupBox4 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox4.setTitle('Message reading test, hex string needs to be filled in')
		self.groupBox4.setGeometry(11, 403, 518, 118)
		self.label16 = QtWidgets.QLabel('Message：', self.groupBox4)
		self.label16.move(9, 30)
		self.textbox13 = QtWidgets.QLineEdit('', self.groupBox4)
		self.textbox13.setGeometry(63, 27, 357, 23)
		self.button26 = QtWidgets.QPushButton('Read', self.groupBox4)
		self.button26.setGeometry(426, 24, 82, 28)
		self.button26.clicked.connect(self.button26_click)
		self.label14 = QtWidgets.QLabel("Result:", self.groupBox4)
		self.label14.move(9, 62)
		self.textbox11 = QtWidgets.QTextEdit('', self.groupBox4)
		self.textbox11.setGeometry(63, 60, 445, 52)
		# groupBox5
		self.groupBox5 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox5.setTitle('Special function test')
		self.groupBox5.setGeometry(546, 243, 419, 278)
		
		self.textbox3 = QtWidgets.QTextEdit('', self.groupBox5)
		self.textbox3.setGeometry(16, 93, 388, 145)

		self.panel2.setEnabled(False)
		self.center()
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2,
				  (screen.height() - size.height()) / 2)
	def button_connect_click(self):
		self.siemens = SiemensS7Net(self.siemensPLCS,self.textboxIp.text())
		self.siemens.port = int(self.textboxPort.text())
		self.siemens.SetSlotAndRack(int(self.textbox15.text()), int(self.textbox16.text()))
		connect = self.siemens.ConnectServer()
		if connect.IsSuccess == False:
			QMessageBox.information(self,'Info','Connect Failed: ' + connect.ToMessageShowString())
		else:
			QMessageBox.information(self,'Info','Connect Success!')
			self.buttonConnect.setEnabled(False)
			self.buttonDisConnect.setEnabled(True)
			self.panel2.setEnabled(True)
			self.userControlReadWriteOp1.SetReadWriteNet(self.siemens, self.Address)
	def button_disconnect_click(self):
		disconnect = self.siemens.ConnectClose()
		if disconnect.IsSuccess == True:
			self.panel2.setEnabled(False)
			self.buttonConnect.setEnabled(True)
			self.buttonDisConnect.setEnabled(False)
		else:
			QMessageBox.information(self,'Info','DisConnect Failed: ' + disconnect.ToMessageShowString())
	def button3_click(self):
		read =self.siemens.ReadOrderNumber()
		if read.IsSuccess == True:
			self.textbox10.setText(datetime.datetime.now().strftime('%H:%M:%S') + " " + read.Content)
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())
	def button25_click(self):
		read = self.siemens.Read(self.textbox6.text(), int(self.textbox9.text()))
		if read.IsSuccess == True:
			self.textbox10.setText(datetime.datetime.now().strftime('%H:%M:%S') + " [" + self.textbox6.text()  + "] "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())
	def button26_click(self):
		read = self.siemens.ReadFromCoreServer(SoftBasic.HexStringToBytes(self.textbox13.text()))
		if read.IsSuccess == True:
			self.textbox11.setText(datetime.datetime.now().strftime('%H:%M:%S') + " "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())

class FormSiemensFetchWriteNet(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.setGeometry(100, 100, WindowsLoad.WindowWidth, WindowsLoad.WindowHeight)                                 # 设置窗体的位置和大小情况
		self.setWindowTitle('西门子PLC访问Demo')                                # 设置窗体的标题
		self.userControlHead = UserControlHead(self)
		self.userControlHead.setGeometry(QtCore.QRect(0, 0, 1004, 32))
		self.userControlHead.setProtocol('Fetch/Write')
		
		self.siemens = None
		self.Address = 'M100'

		self.settings = QtWidgets.QWidget(self)
		self.settings.setGeometry(QtCore.QRect(14, 44, 978, 43))
		self.settings.setObjectName('settings')
		self.settings.setStyleSheet('QWidget#settings{border:1px solid gray;}')
		self.setStyleSheet('FormSiemens{background:#F0F8FF;font:微软雅黑;}')
		self.label1 = QtWidgets.QLabel('Ip：', self.settings)
		self.label1.move(10, 12)
		self.textboxIp = QtWidgets.QLineEdit("", self.settings)
		self.textboxIp.setGeometry(62, 8, 141, 23)
		self.textboxIp.setText('192.168.8.12')
		self.label2 = QtWidgets.QLabel('Port：', self.settings)
		self.label2.move(251, 11)
		self.textboxPort = QtWidgets.QLineEdit("", self.settings)
		self.textboxPort.setGeometry(305, 8, 141, 23)
		self.textboxPort.setText('2000')
		self.buttonConnect = QtWidgets.QPushButton('Connect', self.settings)
		self.buttonConnect.setGeometry(477, 5, 91, 28)
		self.buttonConnect.clicked.connect(self.button_connect_click)
		self.buttonDisConnect = QtWidgets.QPushButton('DisConnect', self.settings)
		self.buttonDisConnect.setGeometry(584, 5, 91, 28)
		self.buttonDisConnect.clicked.connect(self.button_disconnect_click)
		self.buttonDisConnect.setEnabled(False)
		# panel2
		self.panel2 = QtWidgets.QWidget(self)
		self.panel2.setGeometry(14, 99, 978, 537)
		self.panel2.setObjectName('panel2')
		self.panel2.setStyleSheet('QWidget#panel2{border:1px solid gray;}')
		self.userControlReadWriteOp1 = UserControlReadWriteOp(self.panel2)
		self.userControlReadWriteOp1.move(11, 2)
		# groupBox3
		self.groupBox3 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox3.setTitle('Bulk Read test')
		self.groupBox3.setGeometry(11, 243, 518, 154)
		self.label11 = QtWidgets.QLabel('Address：', self.groupBox3)
		self.label11.move(9, 30)
		self.textbox6 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox6.setGeometry(63, 27, 102, 23)
		self.textbox6.setText(self.Address)
		self.label12 = QtWidgets.QLabel('Length：', self.groupBox3)
		self.label12.move(180, 30)
		self.textbox9 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox9.setGeometry(234, 27, 102, 23)
		self.textbox9.setText('10')
		self.button25 = QtWidgets.QPushButton('bulk read', self.groupBox3)
		self.button25.setGeometry(426, 24, 82, 28)
		self.button25.clicked.connect(self.button25_click)
		self.label13 = QtWidgets.QLabel("Result:", self.groupBox3)
		self.label13.move(9, 62)
		self.textbox10 = QtWidgets.QTextEdit("", self.groupBox3)
		self.textbox10.setGeometry(63, 60, 445, 78)
		# groupBox4
		self.groupBox4 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox4.setTitle('Message reading test, hex string needs to be filled in')
		self.groupBox4.setGeometry(11, 403, 518, 118)
		self.label16 = QtWidgets.QLabel('Message：', self.groupBox4)
		self.label16.move(9, 30)
		self.textbox13 = QtWidgets.QLineEdit('', self.groupBox4)
		self.textbox13.setGeometry(63, 27, 357, 23)
		self.button26 = QtWidgets.QPushButton('Read', self.groupBox4)
		self.button26.setGeometry(426, 24, 82, 28)
		self.button26.clicked.connect(self.button26_click)
		self.label14 = QtWidgets.QLabel("Result:", self.groupBox4)
		self.label14.move(9, 62)
		self.textbox11 = QtWidgets.QTextEdit('', self.groupBox4)
		self.textbox11.setGeometry(63, 60, 445, 52)
		# groupBox5
		self.groupBox5 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox5.setTitle('Special function test')
		self.groupBox5.setGeometry(546, 243, 419, 278)
		
		self.textbox3 = QtWidgets.QTextEdit('', self.groupBox5)
		self.textbox3.setGeometry(16, 93, 388, 145)

		self.panel2.setEnabled(False)
		self.center()
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2,
				  (screen.height() - size.height()) / 2)
	def button_connect_click(self):
		self.siemens = SiemensFetchWriteNet(self.textboxIp.text(), int(self.textboxPort.text()))
		connect = self.siemens.ConnectServer()
		if connect.IsSuccess == False:
			QMessageBox.information(self,'Info','Connect Failed: ' + connect.ToMessageShowString())
		else:
			QMessageBox.information(self,'Info','Connect Success!')
			self.buttonConnect.setEnabled(False)
			self.buttonDisConnect.setEnabled(True)
			self.panel2.setEnabled(True)
			self.userControlReadWriteOp1.SetReadWriteNet(self.siemens, self.Address)
	def button_disconnect_click(self):
		disconnect = self.siemens.ConnectClose()
		if disconnect.IsSuccess == True:
			self.panel2.setEnabled(False)
			self.buttonConnect.setEnabled(True)
			self.buttonDisConnect.setEnabled(False)
		else:
			QMessageBox.information(self,'Info','DisConnect Failed: ' + disconnect.ToMessageShowString())
	def button25_click(self):
		read = self.siemens.Read(self.textbox6.text(), int(self.textbox9.text()))
		if read.IsSuccess == True:
			self.textbox10.setText(datetime.datetime.now().strftime('%H:%M:%S') + " [" + self.textbox6.text()  + "] "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())
	def button26_click(self):
		read = self.siemens.ReadFromCoreServer(SoftBasic.HexStringToBytes(self.textbox13.text()))
		if read.IsSuccess == True:
			self.textbox11.setText(datetime.datetime.now().strftime('%H:%M:%S') + " "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())

class FormOmron(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.setGeometry(100, 100, WindowsLoad.WindowWidth, WindowsLoad.WindowHeight)                                 # 设置窗体的位置和大小情况
		self.setWindowTitle('欧姆龙PLC访问Demo')                                # 设置窗体的标题
		self.userControlHead = UserControlHead(self)
		self.userControlHead.setGeometry(QtCore.QRect(0, 0, 1004, 32))
		self.userControlHead.setProtocol('Fins-Tcp')
		
		self.omron = None
		self.Address = 'D100'

		self.settings = QtWidgets.QWidget(self)
		self.settings.setGeometry(QtCore.QRect(14, 44, 978, 54))
		self.settings.setObjectName('settings')
		self.settings.setStyleSheet('QWidget#settings{border:1px solid gray;}')
		self.setStyleSheet('FormOmron{background:#F0F8FF;font:微软雅黑;}')

		self.label1 = QtWidgets.QLabel('Ip：', self.settings)
		self.label1.move(8, 17)
		self.textboxIp = QtWidgets.QLineEdit("", self.settings)
		self.textboxIp.setGeometry(62, 14, 114, 23)
		self.textboxIp.setText('127.0.0.1')

		self.label2 = QtWidgets.QLabel('Port：', self.settings)
		self.label2.move(182, 17)
		self.textboxPort = QtWidgets.QLineEdit("", self.settings)
		self.textboxPort.setGeometry(236, 14, 69, 23)
		self.textboxPort.setText('2000')

		self.label24 = QtWidgets.QLabel('PLC单元号：', self.settings)
		self.label24.move(311, 5)
		self.textbox16 = QtWidgets.QLineEdit("", self.settings)
		self.textbox16.setGeometry(387, 2, 56, 23)
		self.textbox16.setText('0')

		self.label23 = QtWidgets.QLabel('本机网络号：', self.settings)
		self.label23.move(449, 5)
		self.textbox15 = QtWidgets.QLineEdit("", self.settings)
		self.textbox15.setGeometry(525, 2, 56, 23)
		self.textbox15.setText('192')

		self.buttonConnect = QtWidgets.QPushButton('Connect', self.settings)
		self.buttonConnect.setGeometry(690, 11, 64, 28)
		self.buttonConnect.clicked.connect(self.button_connect_click)
		self.buttonDisConnect = QtWidgets.QPushButton('DisConnect', self.settings)
		self.buttonDisConnect.setGeometry(761, 11, 64, 28)
		self.buttonDisConnect.clicked.connect(self.button_disconnect_click)
		self.buttonDisConnect.setEnabled(False)
		# panel2
		self.panel2 = QtWidgets.QWidget(self)
		self.panel2.setGeometry(14, 100, 978, 537)
		self.panel2.setObjectName('panel2')
		self.panel2.setStyleSheet('QWidget#panel2{border:1px solid gray;}')
		self.userControlReadWriteOp1 = UserControlReadWriteOp(self.panel2)
		self.userControlReadWriteOp1.move(11, 2)
		# groupBox3
		self.groupBox3 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox3.setTitle('Bulk Read test')
		self.groupBox3.setGeometry(11, 243, 518, 154)
		self.label11 = QtWidgets.QLabel('Address：', self.groupBox3)
		self.label11.move(9, 30)
		self.textbox6 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox6.setGeometry(63, 27, 102, 23)
		self.textbox6.setText(self.Address)
		self.label12 = QtWidgets.QLabel('Length：', self.groupBox3)
		self.label12.move(180, 30)
		self.textbox9 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox9.setGeometry(234, 27, 102, 23)
		self.textbox9.setText('10')
		self.button25 = QtWidgets.QPushButton('bulk read', self.groupBox3)
		self.button25.setGeometry(426, 24, 82, 28)
		self.button25.clicked.connect(self.button25_click)
		self.label13 = QtWidgets.QLabel("Result:", self.groupBox3)
		self.label13.move(9, 62)
		self.textbox10 = QtWidgets.QTextEdit("", self.groupBox3)
		self.textbox10.setGeometry(63, 60, 445, 78)
		# groupBox4
		self.groupBox4 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox4.setTitle('Message reading test, hex string needs to be filled in')
		self.groupBox4.setGeometry(11, 403, 518, 118)
		self.label16 = QtWidgets.QLabel('Message：', self.groupBox4)
		self.label16.move(9, 30)
		self.textbox13 = QtWidgets.QLineEdit('', self.groupBox4)
		self.textbox13.setGeometry(63, 27, 357, 23)
		self.button26 = QtWidgets.QPushButton('Read', self.groupBox4)
		self.button26.setGeometry(426, 24, 82, 28)
		self.button26.clicked.connect(self.button26_click)
		self.label14 = QtWidgets.QLabel("Result:", self.groupBox4)
		self.label14.move(9, 62)
		self.textbox11 = QtWidgets.QTextEdit('', self.groupBox4)
		self.textbox11.setGeometry(63, 60, 445, 52)
		# groupBox5
		self.groupBox5 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox5.setTitle('Special function test')
		self.groupBox5.setGeometry(546, 243, 419, 278)
		
		self.textbox3 = QtWidgets.QTextEdit('', self.groupBox5)
		self.textbox3.setGeometry(16, 93, 388, 145)

		self.panel2.setEnabled(False)
		self.center()
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2,
				  (screen.height() - size.height()) / 2)
	def button_connect_click(self):
		self.omron = OmronFinsNet(self.textboxIp.text(), int(self.textboxPort.text()))
		self.omron.SA1 = int(self.textbox15.text())
		self.omron.DA2 = int(self.textbox16.text())
		connect = self.omron.ConnectServer()
		if connect.IsSuccess == False:
			QMessageBox.information(self,'Info','Connect Failed: ' + connect.ToMessageShowString())
		else:
			QMessageBox.information(self,'Info','Connect Success!')
			self.buttonConnect.setEnabled(False)
			self.buttonDisConnect.setEnabled(True)
			self.panel2.setEnabled(True)
			self.userControlReadWriteOp1.SetReadWriteNet(self.omron, self.Address)
	def button_disconnect_click(self):
		disconnect = self.omron.ConnectClose()
		if disconnect.IsSuccess == True:
			self.panel2.setEnabled(False)
			self.buttonConnect.setEnabled(True)
			self.buttonDisConnect.setEnabled(False)
		else:
			QMessageBox.information(self,'Info','DisConnect Failed: ' + disconnect.ToMessageShowString())
	def button25_click(self):
		read = self.omron.Read(self.textbox6.text(), int(self.textbox9.text()))
		if read.IsSuccess == True:
			self.textbox10.setText(datetime.datetime.now().strftime('%H:%M:%S') + " [" + self.textbox6.text()  + "] "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())
	def button26_click(self):
		read = self.omron.ReadFromCoreServer(SoftBasic.HexStringToBytes(self.textbox13.text()))
		if read.IsSuccess == True:
			self.textbox11.setText(datetime.datetime.now().strftime('%H:%M:%S') + " "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())


class FormModbus(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()
	def initUI(self):
		self.setGeometry(100, 100, WindowsLoad.WindowWidth, WindowsLoad.WindowHeight)                                 # 设置窗体的位置和大小情况
		self.setWindowTitle('Modbus访问Demo')                                # 设置窗体的标题
		self.userControlHead = UserControlHead(self)
		self.userControlHead.setGeometry(QtCore.QRect(0, 0, 1004, 32))
		self.userControlHead.setProtocol('Modbus-Tcp')
		
		self.modbus = None
		self.Address = '100'

		self.settings = QtWidgets.QWidget(self)
		self.settings.setGeometry(QtCore.QRect(14, 44, 978, 62))
		self.settings.setObjectName('settings')
		self.settings.setStyleSheet('QWidget#settings{border:1px solid gray;}')
		self.setStyleSheet('FormModbus{background:#F0F8FF;font:微软雅黑;}')

		self.label1 = QtWidgets.QLabel('Ip：', self.settings)
		self.label1.move(8, 10)
		self.textboxIp = QtWidgets.QLineEdit('', self.settings)
		self.textboxIp.setGeometry(62, 7, 128, 23)
		self.textboxIp.setText('127.0.0.1')

		self.label2 = QtWidgets.QLabel('Port：', self.settings)
		self.label2.move(196, 10)
		self.textboxPort = QtWidgets.QLineEdit('', self.settings)
		self.textboxPort.setGeometry(250, 7, 76, 23)
		self.textboxPort.setText('502')

		self.label21 = QtWidgets.QLabel('Station：', self.settings)
		self.label21.move(338, 10)
		self.textbox16 = QtWidgets.QLineEdit('', self.settings)
		self.textbox16.setGeometry(392, 7, 39, 23)
		self.textbox16.setText('1')

		self.checkBox1 = QtWidgets.QCheckBox(self.settings)
		self.checkBox1.setText('首地址从0开始')
		self.checkBox1.move(447, 9)
		self.checkBox1.setChecked(True)

		self.comboBox1 = QtWidgets.QComboBox(self.settings)
		self.comboBox1.addItems(['ABCD','BADC','CDAB','DCBA'])
		self.comboBox1.setCurrentIndex(0)
		self.comboBox1.setGeometry(558, 6, 111, 25)

		self.buttonConnect = QtWidgets.QPushButton('Connect', self.settings)
		self.buttonConnect.setGeometry(690, 11, 64, 28)
		self.buttonConnect.clicked.connect(self.button_connect_click)
		self.buttonDisConnect = QtWidgets.QPushButton('DisConnect', self.settings)
		self.buttonDisConnect.setGeometry(761, 11, 64, 28)
		self.buttonDisConnect.clicked.connect(self.button_disconnect_click)
		self.buttonDisConnect.setEnabled(False)
		# panel2
		self.panel2 = QtWidgets.QWidget(self)
		self.panel2.setGeometry(14, 115, 978, 537)
		self.panel2.setObjectName('panel2')
		self.panel2.setStyleSheet('QWidget#panel2{border:1px solid gray;}')
		self.userControlReadWriteOp1 = UserControlReadWriteOp(self.panel2)
		self.userControlReadWriteOp1.move(11, 2)
		# groupBox3
		self.groupBox3 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox3.setTitle('Bulk Read test')
		self.groupBox3.setGeometry(11, 243, 518, 154)
		self.label11 = QtWidgets.QLabel('Address：', self.groupBox3)
		self.label11.move(9, 30)
		self.textbox6 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox6.setGeometry(63, 27, 102, 23)
		self.textbox6.setText(self.Address)
		self.label12 = QtWidgets.QLabel('Length：', self.groupBox3)
		self.label12.move(180, 30)
		self.textbox9 = QtWidgets.QLineEdit('', self.groupBox3)
		self.textbox9.setGeometry(234, 27, 102, 23)
		self.textbox9.setText('10')
		self.button25 = QtWidgets.QPushButton('bulk read', self.groupBox3)
		self.button25.setGeometry(426, 24, 82, 28)
		self.button25.clicked.connect(self.button25_click)
		self.label13 = QtWidgets.QLabel("Result:", self.groupBox3)
		self.label13.move(9, 62)
		self.textbox10 = QtWidgets.QTextEdit("", self.groupBox3)
		self.textbox10.setGeometry(63, 60, 445, 78)
		# groupBox4
		self.groupBox4 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox4.setTitle('Message reading test, hex string needs to be filled in')
		self.groupBox4.setGeometry(11, 403, 518, 118)
		self.label16 = QtWidgets.QLabel('Message：', self.groupBox4)
		self.label16.move(9, 30)
		self.textbox13 = QtWidgets.QLineEdit('', self.groupBox4)
		self.textbox13.setGeometry(63, 27, 357, 23)
		self.button26 = QtWidgets.QPushButton('Read', self.groupBox4)
		self.button26.setGeometry(426, 24, 82, 28)
		self.button26.clicked.connect(self.button26_click)
		self.label14 = QtWidgets.QLabel("Result:", self.groupBox4)
		self.label14.move(9, 62)
		self.textbox11 = QtWidgets.QTextEdit('', self.groupBox4)
		self.textbox11.setGeometry(63, 60, 445, 52)
		# groupBox5
		self.groupBox5 = QtWidgets.QGroupBox(self.panel2)
		self.groupBox5.setTitle('Special function test')
		self.groupBox5.setGeometry(546, 243, 419, 278)
		
		self.textbox3 = QtWidgets.QTextEdit('', self.groupBox5)
		self.textbox3.setGeometry(16, 93, 388, 145)

		self.panel2.setEnabled(False)
		self.center()
	def center(self):
		screen = QDesktopWidget().screenGeometry()
		size = self.geometry()
		self.move((screen.width() - size.width()) / 2,
				  (screen.height() - size.height()) / 2)
	def button_connect_click(self):
		self.modbus = ModbusTcpNet(self.textboxIp.text(), int(self.textboxPort.text()))
		self.modbus.isAddressStartWithZero = self.checkBox1.isChecked()
		if self.comboBox1.currentText() == 'ABCD':
			self.modbus.byteTransform.DataFormat = HslCommunication.DataFormat.ABCD
		elif self.comboBox1.currentText() == 'BADC':
			self.modbus.byteTransform.DataFormat = HslCommunication.DataFormat.BADC
		elif self.comboBox1.currentText() == 'CDAB':
			self.modbus.byteTransform.DataFormat = HslCommunication.DataFormat.CDAB
		elif self.comboBox1.currentText() == 'DCBA':
			self.modbus.byteTransform.DataFormat = HslCommunication.DataFormat.DCBA
		connect = self.modbus.ConnectServer()
		if connect.IsSuccess == False:
			QMessageBox.information(self,'Info','Connect Failed: ' + connect.ToMessageShowString())
		else:
			QMessageBox.information(self,'Info','Connect Success!')
			self.buttonConnect.setEnabled(False)
			self.buttonDisConnect.setEnabled(True)
			self.panel2.setEnabled(True)
			self.userControlReadWriteOp1.SetReadWriteNet(self.modbus, self.Address)
	def button_disconnect_click(self):
		disconnect = self.modbus.ConnectClose()
		if disconnect.IsSuccess == True:
			self.panel2.setEnabled(False)
			self.buttonConnect.setEnabled(True)
			self.buttonDisConnect.setEnabled(False)
		else:
			QMessageBox.information(self,'Info','DisConnect Failed: ' + disconnect.ToMessageShowString())
	def button25_click(self):
		read = self.modbus.Read(self.textbox6.text(), int(self.textbox9.text()))
		if read.IsSuccess == True:
			self.textbox10.setText(datetime.datetime.now().strftime('%H:%M:%S') + " [" + self.textbox6.text()  + "] "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())
	def button26_click(self):
		read = self.modbus.ReadFromCoreServer(SoftBasic.HexStringToBytes(self.textbox13.text()))
		if read.IsSuccess == True:
			self.textbox11.setText(datetime.datetime.now().strftime('%H:%M:%S') + " "+ SoftBasic.ByteToHexString(read.Content))
		else:
			QMessageBox.information(self,'Info','Read Failed: ' + read.ToMessageShowString())

app = QtWidgets.QApplication(sys.argv)
windowsLoad = WindowsLoad()
windowsLoad.show()
sys.exit(app.exec_())