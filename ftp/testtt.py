# -*- coding:utf-8 -*-
'''
ftplib库的读写操作

文件名中含有中文的特殊处理：
收到的为utf-8格式的字符串，在保存时需要使用unicode编码的文件名写入本地文件系统。
测试环境：
Server: File Zilla Server 0.9.50
Client OS: Win7大地

'''
import ftplib
from ftplib import FTP

ftp = ftplib.FTP()
ftp.connect(host='localhost', port=21, timeout=5)  # connect to host, default port
ftp.login(user='honglei', passwd='111111')

# names =[]
# def mycall(line):
# a = [item for item in line.split(" ") if item!=" "]
# name = a[-1]#.decode('utf-8')
# size = a[-5]
# names.append(name)
# ftp.retrlines('LIST',callback=mycall)           # list directory contents
filename = '\xe8\xbf\x99\xe6\x98\xaf\xe4\xb8\xad\xe6\x96\x87.txt'  # 从使用LIST获取到的
ftp.retrbinary('RETR ' + filename, open(filename.decode('utf-8'), 'wb').write)

filename = u"本地待上传的中文文件.txt"
try:
    ftp.storbinary('STOR ' + filename.encode('utf-8'), open(filename, 'rb'))
except ftplib.error_perm as e:
    pass