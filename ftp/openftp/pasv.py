import socket
class PASV:
	DATA_REPLY_BUFFER=4096
	def __init__(self,ipAddress,port):
		self.ipAddress=ipAddress
		self.port=port
	def connectServer(self):
		self.clientSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.clientSock.connect((self.ipAddress,self.port))
	def getCmdData(self):
		return self.clientSock.recv(PASV.DATA_REPLY_BUFFER).strip()
	def getData(self):
		alldata="";
		while True:
			data=self.clientSock.recv(PASV.DATA_REPLY_BUFFER)
			if len(data)!=0:
				alldata+=data
			else:
				break;
		return alldata
	def sendData(self,data):
		self.clientSock.send(data)
	def closeConnect(self):
		self.clientSock.close()
	
