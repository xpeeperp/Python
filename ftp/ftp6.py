#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
'''
使用ftplib编写FTP客户端连接，并指定目录下载。
'''
__author__ = 'sunday208'
__date__ = "2016-02-25 12:50"
import ftplib, socket
from sys import exit
import os


class DOFTP():
    def __init__(self):
        # 定义公用变量
        self.RED_COLOR = '\033[1;31;48m'  # 红 ，配置终端输出的颜色
        self.BLUE_COLOR = '\033[1;34;48m'  # 红 ，配置终端输出的颜色
        self.RES = '\033[0m'

    def FTP_DOWN(self, HostIP, SerPort, FtpUser, FtpPasswd, RootDir, Server_files, Local_dir):
        MyFTP = ftplib.FTP()
        try:
            MyFTP.connect(host=HostIP, port=SerPort, timeout=5)
            print '%s*****已经成功连接"%s"服务器FTP服务！%s' % (self.BLUE_COLOR, HostIP, self.RES)
        except (socket.error, socket.gaierror), e:
            print '%s错误：无法访问"%s" FTP服务，请检查！错误代码为"%s"%s' % (self.RED_COLOR, HostIP, e, self.RES)
            exit()
        try:
            MyFTP.login(user=FtpUser, passwd=FtpPasswd)
            print '%s*****已经成功登陆"%s"服务器FTP服务！%s' % (self.BLUE_COLOR, HostIP, self.RES)
            print MyFTP.getwelcome()  # 显示ftp服务器欢迎信息
        except (ftplib.error_perm), e:
            print '%s错误：登陆失败！，请检查用户名"%s“密码"%s"是否正确！错误代码为"%s"%s' % (self.RED_COLOR, FtpUser, FtpPasswd, e, self.RES)
            exit()
        MyFTP.cwd(RootDir)  # 进入FTP目录
        FTP_files = MyFTP.nlst()  # 取FTP当前目录内容
        if not Server_files:  # 如果要下载为空，将下载该目录全部内容
            DownLists = FTP_files
            print "FTP全部目录%s" % DownLists
        else:
            # 判断指定下载的文件是否在FTP目录中。
            DownLists = []  # 下载列表
            NODownLists = []  # 没有下载列表
            for line in Server_files:
                if line in FTP_files:
                    DownLists.append(line)
                else:
                    NODownLists.append(line)
            if NODownLists:
                print "%s在FTP服务器并没有指定文件%s。%s" % (self.RED_COLOR, ",".join(NODownLists), self.RES)
            if DownLists:
                print "%s正在从FTP服务器下载如下文件%s。%s" % (self.BLUE_COLOR, ",".join(DownLists), self.RES)
        bufsize = 1024
        for line in DownLists:
            FileName = open(Local_dir + line, 'wb').write
            MyFTP.retrbinary('RETR %s' % os.path.basename(line), FileName, bufsize)
        MyFTP.quit()
        print "%sFTP已经成功退出。%s" % (self.BLUE_COLOR, self.RES)


if __name__ == "__main__":
    HostIP = '202.101.231.234'  # FTP服务器IP或者域名
    SerPort = '21'  # FTP端口
    FtpUser = 'testpython'  # FTP用户
    FtpPasswd = 'test123@321'  # FTP对应用户密码
    RootDir = ''  # FTP目录
    Server_files = []  # 下载服务器文件列表
    # Server_files = [] #如果要下载为空，将下载该目录全部内容
    Local_dir = "D:/testtmp/"  # 本地目录
    # Local_files =['a.txt','b.txt']  #上传服务器本地文件列表
    s = DOFTP()
    if os.path.exists(Local_dir) == False:  # 判断本地是否有该文件目录，如果没有，将创建
        try:
            os.mkdir(Local_dir)
            print "%s创建本地目录'%s'%s" % (s.BLUE_COLOR, Local_dir, s.RES)
        except:
            print "%s无法创建本地目录'%s'，原因是无该盘符或者目录路径有问题，程序直接退出！%s" % (s.RED_COLOR, Local_dir, s.RES)
            exit()  # 退出程序

    s.FTP_DOWN(HostIP, SerPort, FtpUser, FtpPasswd, RootDir, Server_files, Local_dir)