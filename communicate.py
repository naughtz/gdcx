import socket

def sendinfo(t,ID,data):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建一个socket
	s.connect((ip, 12000))    #建立连接

	data = t + ID + data
	s.send(data.encode('gb2312'))              #发送编码后的数据
	s.close()  

def getinfo():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创建一个socket
	s.connect((ip, 9888))    #建立连接
	data = s.recv(1024)

	data = data.decode('gb2312')

	s.close()  
	return data