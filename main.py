import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QFont
import json
from Query import *
from communicate import *

import datetime
class MainWindow(QMainWindow):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.statusBar().showMessage('就绪')
		self.createMenu()      	#菜单栏
		self.createButton()    	#按钮
		self.createLabel()	  	#标签
		self.createText()		#文本框
		self.createStyle()		#qss
		self.initial()         	#初始化变量
		self.cardButton.setChecked(True)

		self.clickCardButton()	#初始状态为一卡通查询
		self.setFixedSize(800,500)#设置窗口大小
		self.center()			#窗口居中
		self.setWindowTitle('工大查询')
		self.setWindowIcon(QIcon('./src/pictures/icon.png'))
		self.show()
		try:
			self.inform = getinfo()
			self.informLabel.setText(self.inform)
		except:
			pass

	#初始化变量
	def initial(self):
		self.userinfo = {}		#从userinfo.json读取的信息
		try:
			with open('./user/config.json','r') as f:
				self.config = json.load(f)
		except:
			self.config = {}


	#居中
	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	#皮肤
	def createStyle(self):
		with open('./src/UI/style.qss') as f:
			style = f.read()
		self.setStyleSheet(style)

	#菜单栏
	def createMenu(self):
		self.menubar = self.menuBar()

		self.menu = self.menubar.addMenu("帮助(Help)")
		self.menu.addAction('关于(About)',lambda:QMessageBox.about(self,'关于',
"""V1.2.0
感谢使用！
不会在服务器保存您的密码，请放心使用！
第一次查询成功后会记住密码，这是在您计算机本地保存的！
若发现任何问题或对本软件有任何意见和建议请联系qq1012415775"""))
		self.menu.addAction('版本(Version)',lambda:QMessageBox.about(self,'版本','V1.2.0'))

		self.menu = self.menubar.addMenu("设置(Setup)")
		self.menu.addAction('设置(Setup)',self.Setup)


	#按钮
	def createButton(self):
		self.cardButton = QPushButton('一卡通查询',self)
		self.cardButton.setCheckable(True)
		self.cardButton.setAutoExclusive(True)
		self.cardButton.move(50,50)
		self.cardButton.clicked.connect(self.clickCardButton)
		self.cardButton.setProperty('select',True)
		self.cardButton.setFixedSize(120,40)

		self.gpaButton = QPushButton('成绩查询',self)
		self.gpaButton.setCheckable(True)
		self.gpaButton.setAutoExclusive(True)
		self.gpaButton.move(180,50)
		self.gpaButton.clicked.connect(self.clickGpaButton)
		self.gpaButton.setProperty('select',True)
		self.gpaButton.setFixedSize(120,40)

		self.volunteerButton = QPushButton('志愿信息查询',self)
		self.volunteerButton.setCheckable(True)
		self.volunteerButton.setAutoExclusive(True)
		self.volunteerButton.move(310,50)
		self.volunteerButton.clicked.connect(self.clickVolunteerButton)
		self.volunteerButton.setProperty('select',True)
		self.volunteerButton.setFixedSize(120,40)

		self.dawuButton = QPushButton('大物实验查询',self)
		self.dawuButton.setCheckable(True)
		self.dawuButton.setAutoExclusive(True)
		self.dawuButton.move(440,50)
		self.dawuButton.clicked.connect(self.clickDawuButton)
		self.dawuButton.setProperty('select',True)
		self.dawuButton.setFixedSize(120,40)

		self.dianluButton = QPushButton('电路实验查询',self)
		self.dianluButton.setCheckable(True)
		self.dianluButton.setAutoExclusive(True)
		self.dianluButton.move(570,50)
		self.dianluButton.clicked.connect(self.clickDianluButton)
		self.dianluButton.setProperty('select',True)
		self.dianluButton.setFixedSize(120,40)

		self.confirmButton = QPushButton('确认',self)
		self.confirmButton.move(250,200)
		self.confirmButton.clicked.connect(self.clickConfirmButton)


	#标签
	def createLabel(self):
		self.nameLabel = QLabel(self)
		self.nameLabel.setText('学   号:')
		self.nameLabel.move(100,100)

		self.pwdLabel = QLabel(self)
		self.pwdLabel.setText('查询密码:')
		self.pwdLabel.move(100,150)

		self.msgLabel = QLabel(self)
		self.msgLabel.setText('')
		self.msgLabel.move(120,200)
		self.msgLabel.setProperty('message',True)

		self.informLabel = QLabel(self)
		self.informLabel.setFixedSize(300,150)
		self.informLabel.move(430,100)

	#文本框
	def createText(self):
		self.nameText = QLineEdit(self)
		self.nameText.move(200,100)
		self.nameText.setFixedSize(150,30)

		self.pwdText = QLineEdit(self)
		self.pwdText.move(200,150)
		self.pwdText.setFixedSize(150,30)
		self.pwdText.setEchoMode(QLineEdit.Password)
		self.pwdText.returnPressed.connect(self.clickConfirmButton)

		self.resultText = QTextEdit(self)
		self.resultText.move(30,260)
		self.resultText.setFixedSize(750,180)
		self.resultText.setReadOnly(True)

	#一卡通查询按钮点击事件
	def clickCardButton(self):
		self.state = 'card'
		self.statusBar().showMessage('一卡通查询') 
		self.pwdLabel.setText('查询密码:')
		self.nameText.setText('')
		self.pwdText.setText('')
		self.msgLabel.setText('')
		try:
			with open("./user/userinfo.json","r") as f:
				self.userinfo = json.load(f)
			self.nameText.setText(self.userinfo['card_ID'])
			self.pwdText.setText(self.userinfo['card_pwd'])
			self.pwdText.setFocus()
		except:
			if self.nameText.text() == '':
				self.nameText.setFocus()
			else:
				self.pwdText.setFocus()

	#成绩查询按钮点击事件
	def clickGpaButton(self):
		self.state = 'gpa'
		self.statusBar().showMessage('成绩查询')
		self.pwdLabel.setText('教务系统密码:')
		self.nameText.setText('')
		self.pwdText.setText('')
		self.msgLabel.setText('')
		try:
			with open("./user/userinfo.json","r") as f:
				self.userinfo = json.load(f)
			self.nameText.setText(self.userinfo['jwxt_ID'])
			self.pwdText.setText(self.userinfo['jwxt_pwd'])
			self.pwdText.setFocus()
		except:
			if self.nameText.text() == '':
				self.nameText.setFocus()
			else:
				self.pwdText.setFocus()

	#志愿信息查询按钮点击事件
	def clickVolunteerButton(self):
		self.state = 'volunteer'
		self.statusBar().showMessage('志愿信息查询')
		self.pwdLabel.setText('志愿信息密码:')
		self.nameText.setText('')
		self.pwdText.setText('')
		self.msgLabel.setText('')
		try:
			with open("./user/userinfo.json","r") as f:
				self.userinfo = json.load(f)
			self.nameText.setText(self.userinfo['volunteer_ID'])
			self.pwdText.setText(self.userinfo['volunteer_pwd'])
			self.pwdText.setFocus()
		except:
			if self.nameText.text() == '':
				self.nameText.setFocus()
			else:
				self.pwdText.setFocus()

	#大物实验查询按钮点击事件
	def clickDawuButton(self):
		self.state = 'dawu'
		self.statusBar().showMessage('大物实验查询')
		self.pwdLabel.setText('大物实验密码:')
		self.nameText.setText('')
		self.pwdText.setText('')
		self.msgLabel.setText('')
		try:
			with open("./user/userinfo.json","r") as f:
				self.userinfo = json.load(f)
			self.nameText.setText(self.userinfo['dawu_ID'])
			self.pwdText.setText(self.userinfo['dawu_pwd'])
			self.pwdText.setFocus()
		except:
			if self.nameText.text() == '':
				self.nameText.setFocus()
			else:
				self.pwdText.setFocus()

	#电路实验查询按钮点击事件
	def clickDianluButton(self):
		self.state = 'dianlu'
		self.statusBar().showMessage('电路实验查询')
		self.pwdLabel.setText('电路实验密码:')
		self.nameText.setText('')
		self.pwdText.setText('')
		self.msgLabel.setText('')
		try:
			with open("./user/userinfo.json","r") as f:
				self.userinfo = json.load(f)
			self.nameText.setText(self.userinfo['dianlu_ID'])
			self.pwdText.setText(self.userinfo['dianlu_pwd'])
			self.pwdText.setFocus()
		except:
			if self.nameText.text() == '':
				self.nameText.setFocus()
			else:
				self.pwdText.setFocus()

	#确认按钮点击事件
	def clickConfirmButton(self):
		self.msgLabel.setText('')
		self.name = self.nameText.text().replace(' ','')
		self.pwd = self.pwdText.text().replace(' ','')
		#一卡通查询
		if self.state == 'card':
			cardinfo,ok = cardQuery(self.name,self.pwd)
			if ok==False:
				self.msgLabel.setText('查询失败')
				self.pwdText.selectAll()
				return
			else:
				j = 0  #记录条数
				string = ''
				for i in cardinfo:
					j += 1
					if j%10 == 0:
						string += '\n'
					if j%10==2 or j%10==3 or j%10==0:
						continue
					if j%10 == 5:
						i = i.replace(' ','')
						if len(i)<=5:
							i += '\t'

					string += i + '\t'
					
				string += '以上为当日消费记录\n更多信息前往http://172.26.11.254/homeLogin.action查询\n'
				self.resultText.setText(string)
				self.userinfo['card_ID'] = self.name
				self.userinfo['card_pwd'] = self.pwd
				with open("./user/userinfo.json","w") as f:
					json.dump(self.userinfo,f)

				if self.config['card_share']:
					try:
						sendinfo('card',self.name+datetime.date.today().isoformat(),str(cardinfo))
					except:
						pass

		#成绩查询
		if self.state == 'gpa':
			gpainfo,ok = gpaQuery(self.name,self.pwd)
			#--计算学分绩
			score = 0
			point = 0
			#--
			if ok==False:
				self.msgLabel.setText('查询失败')
				self.pwdText.selectAll()
				return
			else:
				j = 0
				string = '课程名\t\t学分\t考试时间\t总成绩\t考试类型\n'
				for i in gpainfo:
					j += 1
					if j%13==2 or j%13==4 or j%13==5 or j%13==10 or j%13==12:
						string += i[:9]+'\t'
					if j%13==2:
						if len(i)<=5:
							string += '\t'
					if j%13==12:
						if i=='考试':
							try:
								point += float(gpainfo[j-9])
								score += float(gpainfo[j-9])*float(gpainfo[j-3])
							except:
								pass
					if j%13==0:
						string += '\n'
				string = '学分绩(保研算法): ' + str(score/point) + '\n' + string
				string += '更多信息前往http://222.194.15.1:7777/zhxt_bks/zhxt_bks.html查询\n'
				self.resultText.setText(string)
				self.userinfo['jwxt_ID'] = self.name
				self.userinfo['jwxt_pwd'] = self.pwd
				with open("./user/userinfo.json","w") as f:
					json.dump(self.userinfo,f)

				if self.config['gpa_share']:
					try:
						sendinfo('gpa',self.name,str(score/point))
					except:
						pass

		#志愿信息查询
		if self.state=='volunteer':
			volunteerinfo,ok = volunteerQuery(self.name,self.pwd)
			time = 0 #计算总志愿时长
			if ok==False:
				self.msgLabel.setText('查询失败')
				self.pwdText.selectAll()
				return
			else:
				j = 0
				string = '序号\t服务名称\t\t\t志愿时长\t服务评价\n'
				for i in volunteerinfo:
					j += 1
					if j%3==1:
						string += str(int((j+2)/3)) + '\t'
					string += i + '\t'
					if j%3==1:
						if len(i)<=5:
							string+='\t\t'
						elif len(i) <=10:
							string+='\t'
					if j%3==2:
						time += float(i)
					if j%3==0:
						string += '\n'

				string = '总志愿时长: ' + str(time) + '\n' + string
				string += '更多信息前往http://volunteer.hitwh.edu.cn/VolLogin.asp查询\n'
				self.resultText.setText(string)
				self.userinfo['volunteer_ID'] = self.name
				self.userinfo['volunteer_pwd'] = self.pwd
				with open("./user/userinfo.json","w") as f:
					json.dump(self.userinfo,f)

		#大物实验查询
		if self.state=='dawu':
			dawuinfo,scoreinfo,ok = dawuQuery(self.name,self.pwd)

			if ok==False:
				self.msgLabel.setText('查询失败')
				self.pwdText.selectAll()
				return
			else:
				j = 0
				flag = 0
				subject = ''
				string = ''

				for i in dawuinfo:
					j += 1
					string += i[:9] + '\t'
					if j%7==3 and j!=3 or j==2:
						if len(i)<=5:
							string += '\t'
					if j!=2 and j%7==2:
						if i in scoreinfo:
							flag = 1
							subject = i
					if j!=1 and j%7==1:
						if flag==1:
							string += str(scoreinfo[scoreinfo.index(subject)+1])
							flag = 0
						string += '\n'

				
				string += '更多信息前往http://10.246.255.9查询\n'
				self.resultText.setText(string)
				self.userinfo['dawu_ID'] = self.name
				self.userinfo['dawu_pwd'] = self.pwd
				with open("./user/userinfo.json","w") as f:
					json.dump(self.userinfo,f)

		#电路实验查询
		if self.state == 'dianlu':
			dianluinfo,ok = dianluQuery(self.name,self.pwd)
			if ok==False:
				self.msgLabel.setText('查询失败')
				self.pwdText.selectAll()
				return
			else:
				j = 0
				string = '实验名称\t\t\t上课时间\t\t\t\t操作成绩\t报告成绩\n'
				for i in dianluinfo:
					j += 1
					if j%5==1:
						i = i[:14]
					string += i + '\t'
					if j%5==0:
						string += '\n'
					if j%5==2 or j%5==3:
						if len(i)<=5:
							string += '\t'

				string += '更多信息前往http://eelab.hitwh.edu.cn/index.asp查询\n'
				self.resultText.setText(string)
				self.userinfo['dianlu_ID'] = self.name
				self.userinfo['dianlu_pwd'] = self.pwd
				with open("./user/userinfo.json","w") as f:
					json.dump(self.userinfo,f)

	#设置
	def Setup(self):
		self.setupWindow = QMdiSubWindow()
		self.setupWindow.setWindowTitle('设置')
		self.setupWindow.setFixedSize(280,200)
		self.setupWindow.setWindowIcon(QIcon('./src/pictures/setup.png'))

		try:
			with open('./user/config.json','r') as f:
				self.config = json.load(f)
		except:
			self.config = {}

		self.setupWindow.gpaShareLabel = QLabel(self.setupWindow)
		self.setupWindow.gpaShareLabel.move(30,20)
		self.setupWindow.gpaShareLabel.setText('分享学分绩')
		self.setupWindow.gpaShareBox = QCheckBox(self.setupWindow)
		self.setupWindow.gpaShareBox.move(120,20)
		try:
			if self.config['gpa_share']:
				self.setupWindow.gpaShareBox.setChecked(True)
		except:
			pass

		self.setupWindow.cardShareLabel = QLabel(self.setupWindow)
		self.setupWindow.cardShareLabel.move(30,50)
		self.setupWindow.cardShareLabel.setText('分享消费额')
		self.setupWindow.cardShareBox = QCheckBox(self.setupWindow)
		self.setupWindow.cardShareBox.move(120,50)
		try:
			if self.config['card_share']:
				self.setupWindow.cardShareBox.setChecked(True)
		except:
			pass

		self.setupWindow.saveButton = QPushButton(self.setupWindow)
		self.setupWindow.saveButton.setFixedSize(60,40)
		self.setupWindow.saveButton.move(120,150)
		self.setupWindow.saveButton.setText('保存')
		self.setupWindow.saveButton.clicked.connect(self.saveConfig)

		self.setupWindow.cancelButton = QPushButton(self.setupWindow)
		self.setupWindow.cancelButton.setFixedSize(60,40)
		self.setupWindow.cancelButton.move(190,150)
		self.setupWindow.cancelButton.setText('取消')
		self.setupWindow.cancelButton.clicked.connect(lambda:self.setupWindow.close())

		self.setupWindow.show()

	#保存设置信息
	def saveConfig(self):
		if self.setupWindow.gpaShareBox.checkState():
			self.config['gpa_share'] = True
		else:
			self.config['gpa_share'] = False
		if self.setupWindow.cardShareBox.checkState():
			self.config['card_share'] = True
		else:
			self.config['card_share'] = False
		with open('./user/config.json','w') as f:
			json.dump(self.config,f)
		self.setupWindow.close()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	mainWindow = MainWindow()
	sys.exit(app.exec_())