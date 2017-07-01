# !/usr/bin/python
# coding:utf-8
# write:JACK
# info:ftp example
import ftplib, socket, os
from time import sleep, ctime


def LoginFtp(self):
    ftps = ftplib.FTP()
    ftps.connect(self.host, self.port)
    ftps.login(self.name, self.passwd)


# 未进行判断地址输入是否为ip或者域名；可以进行判断是否包含<或者实体符号以及'；其他可以忽略
class LoFtp(object):
    'this is ftp class example'
    host = str(raw_input('host,202.101.231.234\n'))
    if host == '': host = '202.101.231.234'

    port = raw_input('port,21\n')
    if not (port.isdigit()): port = 21

    name = str(raw_input('name,anonymous\n'))
    if name == '': name = 'testpython'

    passwd = str(raw_input('password\n'))
    if passwd == '': passwd = 'test123@321' \
                              ''

    def ZqFtp(self, host, name, passwd, port):
        self.host = host
        self.name = name
        self.passwd = passwd
        self.port = port

    def LoginFtp(self):
        self.ftps = ftplib.FTP()
        self.ftps.connect(self.host, self.port)
        self.ftps.login(self.name, self.passwd)
        self.buffer = 2048  # 设置缓存大小

    def ShowFtp(self):
        self.LoginFtp()
        self.ftps.dir('/')
        dirs = str(raw_input('PLEASE INPUT DIR!\n'))
        print self.ftps.dir(dirs)

    def UpFtp(self):
        'uploads files'
        self.LoginFtp()
        self.ftps.set_debuglevel(2)
        filename = str(raw_input('PLEASE FILE NAME!\n'))
        file_open = open(filename, 'rb')  # 打开文件 可读即可
        self.ftps.storbinary('STOR %s' % os.path.basename(filename), file_open, self.buffer)
        # 上传文件
        self.ftps.set_debuglevel(0)
        file_open.close()

    def DelFtp(self):
        'Delete Files'
        self.LoginFtp()
        filename = str(raw_input('PLEASE DELETE FILE NAME!\n'))
        self.ftps.delete(filename)

    def RemoveFtp(self):
        'Remove File'
        self.LoginFtp()
        self.ftps.set_debuglevel(2)  # 调试级别，0无任何信息提示
        oldfile = str(raw_input('PLEASE OLD FILE NAME!\n'))
        newfile = str(raw_input('PLEASE NEW FILE NAME!\n'))
        self.ftps.rename(oldfile, newfile)
        self.ftps.set_debuglevel(0)

    def DownFtp(self):
        'Download File'
        self.LoginFtp()
        self.ftps.set_debuglevel(2)
        filename = str(raw_input('PLEASE FILE NAME!\n'))
        file_down = open(filename, 'wb').write
        self.ftps.retrbinary('STOP %s' % os.path.basename(filename), file_down, self.buffer)
        self.ftps.set_debuglevel(0)
        file_down.close()


a = LoFtp()
print a.ShowFtp()

while True:
    helpn = str(raw_input('Whether to continue to view or exit immediately!(y/n/q)\n'))
    if (helpn == 'y') or (helpn == 'Y'):
        dirs = str(raw_input('PLEASE INPUT DIR!\n'))
        a.ftps.dir(dirs)
    elif (helpn == 'q') or (helpn == 'Q'):
        exit()
    else:
        break

while True:
    print '上传请选择----1'
    print '下载请选择----2'
    print '修改FTP文件名称----3'
    num = int(raw_input('PLEASE INPUT NUMBER![exit:5]\n'))

    if num == 1:
        upf = a.UpFtp()
        print 'Upfile ok!'
    elif num == 2:
        dof = a.DownFtp()
        print 'Download file ok!'
    elif num == 3:
        ref = a.RemoveFtp()
        print 'Remove file ok!'
    else:
        a.ftps.quit()
        print 'Bingo!'
        break


        # login(user='anonymous',passwd='', acct='') 登录到FTP服务器，所有的参数都是可选的
        # pwd()                                     得到当前工作目录
        # cwd(path)                                 把当前工作目录设置为path
        # dir([path[,...[,cb]])       显示path目录里的内容，可选的参数cb 是一个回调函数，它会被传给retrlines()方法
        # nlst([path[,...])           与dir()类似，但返回一个文件名的列表，而不是显示这些文件名
        # retrlines(cmd [, cb])       给定FTP 命令（如“RETR filename”），用于下载文本文件。可选的回调函数cb 用于处理文件的每一行
        # retrbinary(cmd, cb[,bs=8192[, ra]])        与retrlines()类似，只是这个指令处理二进制文件。回调函数cb 用于处理每一块（块大小默认为8K）下载的数据。
        # storlines(cmd, f)           给定FTP 命令（如“STOR filename”），以上传文本文件。要给定一个文件对象f
        # storbinary(cmd, f[,bs=8192])               与storlines()类似，只是这个指令处理二进制文件。要给定一个文件对象f，上传块大小bs 默认为8Kbs=8192])
        # rename(old, new)            把远程文件old 改名为new
        # delete(path)                删除位于path 的远程文件
        # mkd(directory)              创建远程目录
        # 每个需要输入的地方，需要进行排查检错。仅仅这个功能太小了。不过根据实际情况更改，放在bt里边当个小工具即可
        # 有点烂，没有做任何try