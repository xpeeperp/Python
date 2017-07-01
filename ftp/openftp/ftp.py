import socket
import string
import pasv
class ftp:
	CMD_REPLY_BUFFER=1024
	#Initialize 
	def __init__(self):
		#PASV|PORT
		self.transferMode="PASV"
		#BINARY|ASCII
		self.dataMode="BINARY"
		#STANDARD|ZLIB
		self.dataCompressMode="STANDARD"
		self.debugMode=True
	#Some settings here
	def setTransferMode(self,transferMode):
		self.transferMode=transferMode
	def setDataMode(self,dataMode):
		self.dataMode=dataMode
		if dataMode =="ASCII" or dataMode=="BINARY":
			if dataMode=="ASCII":
				info="TYPE A"
			elif dataMode=="BINARY":
				info="TYPE I"
		else:
			print "Unknown Datatype!"	
			return
		self.handle(info)
	def setDataCompressMode(self,dataCompressMode):
		self.dataCompressMode=dataCompressMode
		if dataCompressMode=="STANDARD" or dataCompressMode=="ZLIB":
			if dataCompressMode=="STANDARD":
				info="MODE S"
			elif dataCompressMode=="ZLIB":
				info="MODE Z"
		else:
			print 'Unknown Compress Mode!'
		self.dataCompressMode=dataCompressMode
		self.handle(info)
	def setDebugMode(self,debugMode):
		self.debugMode=debugMode
	#Some common methods
	def sendRequest(self,info):
		self.sock.send(info+"\r\n")
		if(self.debugMode==True):
			print '[Send]:'+info
	def recvResponse(self):
		self.getReturnInfo()
		print self.info
	def handle(self,info):
		self.sendRequest(info)
		self.recvResponse()
	#Build the command connection with the remote FTP server
	def open(self,address,port):
		self.address=address
		self.port=port
		self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.connect((address,port))
		self.recvResponse()
	#Send the username to login
	def username(self,username):
		self.username=username
		info='USER'+' '+self.username
		self.handle(info)
	#Send the userpassword to login
	def password(self,userpass):
		self.userpass=userpass
		info='PASS'+' '+self.userpass
		self.handle(info)
	#Change the current user's working dir to remotedir on the remote FTP server
	def changedir(self,remotedir):
		self.remotedir=remotedir
		info='CWD'+' '+self.remotedir
		self.handle(info)
	#Back to the upper dir
	def changedirup(self):
		info='CDUP'
		self.handle(info)
	#Return the current user's working dir on the remote FTP server
	def getcurrentdir(self):
		info='PWD'
		self.handle(info)
	#Send the PASV command to get the PASV Mode parameters
	def pasv(self):
		info='PASV'
		self.handle(info)
		self.pasvInfo=self.info[:];
	#To list the current dir on the remote FTP server
	def dir(self,param):
		self.pasv()
		self.getPASVInfo(self.pasvInfo)
		p=pasv.PASV(self.remoteIPAddress,self.remoteDataPort)
		p.connectServer()
		if param is None:
			info='LIST'
		else:
			info='LIST'+' '+param
		self.handle(info)
		getInfo=p.getCmdData()
		p.closeConnect()
		print getInfo
		self.recvResponse()
	 
	#Upload a file ,if it exists on server ,overwrite it if overwrite is True
	def uploadfile(self,filename,newfilename,overwrite):
		self.pasv()
		self.getPASVInfo(self.pasvInfo)
		p=pasv.PASV(self.remoteIPAddress,self.remoteDataPort)
		p.connectServer()
		if overwrite ==True:
			info="STOR"+" "+newfilename
		else:
			info="STOU"+" "+newfilename
		self.handle(info)
		if(self.dataMode=="ASCII"):
			f=file(filename,"r")
		else:
			f=file(filename,"rb")
		while True:
			line=f.readline()
			if len(line)==0:
				p.closeConnect()
				break;
			p.sendData(line)
		f.close()
		self.recvResponse()
	#append a file
	def appendfile(self,localfilename,remotefilename):
		try:
			f=file(localfilename)
		except IOError:
			print 'Local File Read Wrong!'
			return
		self.pasv()
		self.getPASVInfo(self.pasvInfo)
		p=pasv.PASV(self.remoteIPAddress,self.remoteDataPort)
		p.connectServer()
		info="APPE"+" "+remotefilename
		self.handle(info)
		if(self.getcode(self.info)=="550"):
			return
		if(self.dataMode=="ASCII"):
			f=file(localfilename,"r")
		else:
			f=file(localfilename,"rb")
		while True:
			line=f.readline()
			if len(line)==0:
				p.closeConnect()
				break;
			p.sendData(line)
		f.close()
		self.recvResponse()
	#Download a file
	def downloadfile(self,filename,newfilename):
		self.pasv()
		self.getPASVInfo(self.pasvInfo)
		p=pasv.PASV(self.remoteIPAddress,self.remoteDataPort)
		p.connectServer()
		info="RETR"+" "+filename
		self.handle(info)
		if(self.getcode(self.info)=="550"):
			return
		data=p.getData()
		self.recvResponse()
		if(self.dataMode=="ASCII"):
			f=file(newfilename,"w")
		else:
			f=file(newfilename,"wb")
		f.write(data)
		f.close()
	#Delete a file
	def deletefile(self,filename):
		info='DELE'+" "+filename
		self.handle(info)
	#Remove a directory
	def removedir(self,dirname):
		info="RMD"+" "+dirname
		self.handle(info)
	#Rename a file or directory
	def rename(self,old,new):
		info="RNFR"+" "+old
		self.handle(info)
		if(self.getcode(self.info)=="550"):
			return
		info="RNTO"+" "+new
		self.handle(info)
	#Create a directory
	def createdir(self,dirname):
		info="MKD"+" "+dirname
		self.handle(info)
	#Get file size
	def getfilesize(self,filename):
		info="SIZE"+" "+filename
		self.handle(info)
	#Get system type
	def getserversystemtype(self):
		info="SYST"
		self.handle(info)
	#Get the remote server ip address and data port from the returned info of command PASV
	def getPASVInfo(self,pasvinfo):
		start=pasvinfo.index('(')
		end=pasvinfo.index(')')
		substr=pasvinfo[start+1:end]
		parts=substr.rsplit(',')
		self.remoteIPAddress=parts[0]+"."+parts[1]+"."+parts[2]+"."+parts[3]
		self.remoteDataPort=int(parts[4])*256+int(parts[5])
	#Get remotehelp list
	def getremotehelp(self,helpcmd):
		if helpcmd is None:
			info="HELP"
		else:
			info="HELP"+" "+helpcmd
		self.handle(info)
	#Quit the connection
	def disconnect(self):
		info="QUIT"
		self.handle(info)
	#Get the return info from the remote FTP server
	def getReturnInfo(self):
		self.info=""
		tmpinfo=""
		tmpinfo=self.sock.recv(ftp.CMD_REPLY_BUFFER).strip()
		self.info+=tmpinfo[:]
		code=self.getcode(tmpinfo)
		
		while(tmpinfo[3]=="-" and tmpinfo.count(code+" ")==0):
			tmpinfo=""
			tmpinfo=self.sock.recv(ftp.CMD_REPLY_BUFFER).strip()
			code=self.getcode(tmpinfo)
			self.info+="\r\n"+tmpinfo[:]
	#get the return ftp reply code
	def getcode(self,str):
		return str[0:3]
	 
		
