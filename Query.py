import json
import requests
import re

def cardQuery(ID,pwd):
	try:
		data = {
			'name': ID,
			'userType': '1',
			'passwd': pwd,
			'loginType': '2',
		}

		r = requests.session()
		r.post('http://172.26.11.254/loginstudent.action',data=data)
		res = r.get('http://172.26.11.254/accountcardUser.action')
		if re.findall(r'<title>(.*?)</title>',res.text)[0]=='信息提示':
			return (False,False)

		des = res.text.find('<td width="10%" class="neiwen">')
		account = res.text[des+82:des+86]      #一卡通账号
		data2 ={
			'account': account,
			'inputObject': 'all',
		}

		res = r.post('http://172.26.11.254/accounttodatTrjnObject.action',data=data2)

		cardinfo = re.findall(r'<td *align=".*?".*?>(.*?)</td>',res.text)

		return (cardinfo,True)
	except:
		return (False,False)

def gpaQuery(ID,pwd):
	try:
		data = {
			'stuid': ID,
			'pwd': pwd,
		}
		r = requests.session()
		r.post('http://222.194.15.1:7777/pls/wwwbks/bks_login2.login',data=data)
		res = r.get('http://222.194.15.1:7777/pls/wwwbks/bkscjcx.yxkc')
		gpainfo = re.findall(r'<td width="112" height="20" class=td_biaogexian><p align="center">(.*?)</p></td>',res.text)

		if len(gpainfo)==0:
			return (False,False)
		else:
			return (gpainfo,True)
	except:
		return (False,False)

def volunteerQuery(ID,pwd):
	try:
		data = {
			'VolStudentID': ID,
			'Password': pwd,
			'Submit': '',
		}
		r = requests.session()
		res = r.post('http://volunteer.hitwh.edu.cn/Vol_ChkLogin.asp',data=data)
		if res.text.find("<script language='javascript'>alert('学号或密码错误，请重新登录！');location.href='javascript:history.go(-1)';</script>")!=-1:
			return (False,False)
		res = r.get('http://volunteer.hitwh.edu.cn/Individual.asp')
		
		volunteerinfo = re.findall(r'<td style="BORDER-bottom: #E7E7E7 1px solid">(.*?)</td>',res.text)
		return (volunteerinfo,True)
	except:
		return (False,False)

def dawuQuery(ID,pwd):
	try:
		data = {
			'name': ID,
			'pwd': pwd,
		}
		r = requests.session()
		res = r.post('http://10.246.255.9/booking/css/forlogin.aspx',data=data)
		if res.text!='yes':
			return (False,False,False)

		res = r.get('http://10.246.255.9/booking/showbooking.aspx')

		dawuinfo = re.findall(r'<td>(.*?)</td>',res.text)

		res = r.get('http://10.246.255.9/booking/showscores.aspx')
		scoreinforaw = re.findall(r'<td>(.*?)</td>',res.text)
		del dawuinfo[7]
		dawuinfo.insert(7,'成绩')
		scoreinfo = []
		j = 0

		for i in scoreinforaw:
			j += 1
			if j!=1 and j%3==1:
				scoreinfo.append(i)
				scoreinfo.append(int(scoreinforaw[j+1]))
		xulunmax = max(scoreinfo[1],scoreinfo[3],scoreinfo[5],scoreinfo[7])
		scoreinfo[1],scoreinfo[3],scoreinfo[5],scoreinfo[7] = xulunmax,xulunmax,xulunmax,xulunmax

		return (dawuinfo,scoreinfo,True)
	except:
		return (False,False,False)

def dianluQuery(ID,pwd):
	try:
		data = {
			'student': ID,
			'password': pwd,
		}
		r = requests.session()
		res = r.post('http://eelab.hitwh.edu.cn/xk/index.asp',data=data)
		res = r.get('http://eelab.hitwh.edu.cn/xk/CKKB.asp')
		
		timeinfo = re.findall(r'<strong>(.*?)</strong>',res.content.decode('gb2312'))

		j = 0
		for i in timeinfo:
			if j%2==1:
				timeinfo[timeinfo.index(i)] = re.findall(r'"style1">(.*?)</span>',i)[0]
			j+=1
		
		res = r.get('http://eelab.hitwh.edu.cn/xk/CJCX.asp')
		nameinfo = re.findall(r'<TD  height=30>・电路C (.*?)</TD>',res.content.decode('gb2312'))
		scoreinfo = re.findall(r'<TD ><div align="center">(.*?)</div></TD>',res.content.decode('gb2312'))

		dianluinfo = []

		for j in range(0,len(nameinfo)):
			dianluinfo.append(nameinfo[j])
			try:
				dianluinfo.append(timeinfo[2*j])
				dianluinfo.append(timeinfo[2*j+1])
			except:
				dianluinfo.append('待定')
				dianluinfo.append('待定')
			dianluinfo.append(scoreinfo[2*j])
			dianluinfo.append(scoreinfo[2*j+1])

		if len(dianluinfo)==0:
			return (False,False)
		return (dianluinfo,True)
	except:
		return (False,False)
