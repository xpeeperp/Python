# coding=utf-8
'''
	ftp自动下载、自动上传脚本，可以递归目录操作
'''

from ftplib import FTP
import os, sys, string, datetime, time
import socket

#encode=['UTF-8','gbk','GB2312','GB18030','Big5','HZ']
class MYFTP:
    def __init__(self, rootdir_local, hostaddr, username, password, remotedir, port=21):
        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir = remotedir
        self.port = port
        self.ftp = FTP()
        self.file_list = []
        self.rootdir_local = rootdir_local
        self.local_files = []
        self.remote_files = []
        self.appendFiles = []

    # self.ftp.set_debuglevel(2)
    def __del__(self):
        self.ftp.close()

    # self.ftp.set_debuglevel(0)
    def login(self):
        ftp = self.ftp
        try:
            timeout = 300
            socket.setdefaulttimeout(timeout)
            ftp.encoding = self.code
            ftp.set_pasv(True)
            print u'开始连接到 %s' % (self.hostaddr)
            ftp.connect(self.hostaddr, self.port)
            print u'成功连接到 %s' % (self.hostaddr)
            print u'开始登录到 %s' % (self.hostaddr)
            ftp.login(self.username, self.password)
            print u'成功登录到 %s' % (self.hostaddr)
            debug_print(ftp.getwelcome())
        except Exception:
            print u'连接或登录失败'
        try:
            ftp.cwd(self.remotedir)
        except(Exception):
            print u'切换目录失败'

    def margeFile(self):
        temp = []
        try:
            for f in self.remote_files:
                if f in self.local_files:
                    temp.append(f)
            for f in temp:
                self.remote_files.remove(f)
        except Exception, e:
            print e

    def get_localFileList(self, fileTxt):
        print u'从 %s 中读取本地文件列表' % (self.rootdir_local + '/' + fileTxt)
        try:
            fileTxt = open(rootdir_local + '/' + fileTxt, 'r')
        except Exception, e:
            print e
        for line in fileTxt:
            line = line.strip('\n')
            line = line.strip(' ')
            self.local_files.append(line)

    def update_localFileList(self, fileTxt):
        print u'更新 %s 中文件列表' % (self.rootdir_local + '/' + fileTxt)
        try:
            fileTxt = open(rootdir_local + '/' + fileTxt, 'a')
            fileTxt.writelines(['%s\n' % (x) for x in self.appendFiles])
        except Exception, e:
            print e

    def get_remoteFileList(self):
        print u'读取服务器文件列表'
        try:
            self.remote_files = self.ftp.nlst()
        except Exception, e:
            print e

    def download_file(self, localfile, remotefile):
        debug_print(u'>>>>>>>>>>>>下载文件 %s <<<<<<<<<<<<' % localfile)
        # return
        file_handler = open(localfile, 'wb')
        self.ftp.retrbinary(u'RETR %s' % (remotefile.decode('utf-8')), file_handler.write)
        file_handler.close()
        self.appendFiles.append(remotefile.decode('utf-8'))

    def download_marge_files(self):
        for f in self.remote_files:
            self.download_file(rootdir_local + '/' + f, f)

    def download_files(self, localdir='./', remotedir='./'):
        try:
            self.ftp.cwd(remotedir)
        except Exception, e:
            debug_print(u'目录%s不存在，继续...' %remotedir)
            return
        if not os.path.isdir(localdir.decode('utf-8')):
            os.makedirs(localdir.decode('utf-8'))
        debug_print(u'切换至目录 %s' %self.ftp.pwd())
        #得到保存目录名和文件名的数组.
        dir_res = []
        self.ftp.dir("", dir_res.append)
        remotenames = [(f[0],f.split(None, 8)[-1]) for f in dir_res]
        print remotenames
        #remotenames= (files, dirs)
        #print(remotenames)
        #return
        for item in remotenames:
            filetype = item[0]
            filename = item[1]
            local = os.path.join(localdir, filename)
            if filetype == 'd':
                self.download_files(local, filename.decode('utf-8'))
            elif filetype == '-':
                self.download_file(local, filename.decode('utf-8'))
        self.ftp.cwd('..')
        debug_print(u'返回上层目录 %s' %self.ftp.pwd())

    def upload_file(self, localfile, remotefile):
        if not os.path.isfile(localfile):
            return
        if self.is_same_size(localfile, remotefile):
            debug_print(u'跳过[相等]: %s' %localfile)
            return
        file_handler = open(localfile, 'rb')
        self.ftp.storbinary('STOR %s' %remotefile, file_handler)
        file_handler.close()
        debug_print(u'已传送: %s' %localfile)
    def upload_files(self, localdir='./', remotedir = './'):
        if not os.path.isdir(localdir):
            return
        localnames = os.listdir(localdir)
        self.ftp.cwd(remotedir)
        for item in localnames:
            src = os.path.join(localdir, item)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(item)
                except:
                    debug_print(u'目录已存在 %s' %item)
                self.upload_files(src, item)
            else:
                self.upload_file(src, item)
        self.ftp.cwd('..')

    def get_file_list(self, line):
        your_list = []
        # ftp.dir() 命令会列出目录中的文件
        self.ftp.dir("", your_list.append)
        for x in your_list:
            if file_arr[1] not in ['.', '..']:
                self.file_list.append(file_arr)
            filename = x.split()[5:8]  # 或者filename = x.split("\t")[列的起始值:列的终止值]
            filename2 = x.split()[8:9]
            self.file_list
        print (filename)
        ret_arr = []
        file_arr = self.get_filename(line)


def debug_print(s):
    print s



if __name__ == '__main__':
    timenow = time.localtime()
    datenow = time.strftime('%Y-%m-%d', timenow)
    # 配置如下变量
    hostaddr = '202.101.231.234'  # ftp地址
    username = 'testpython2'  # 用户名
    password = 'test123@321'  # 密码
    port = 21  # 端口号
    rootdir_local = 'E:/temp/12'  # 本地目录
    rootdir_remote = '/'  # 远程目录
    local_file_list_txt = 'fileList.txt'
    #while:
    f = MYFTP(rootdir_local, hostaddr, username, password, rootdir_remote, port)
    f.login()
    f.get_localFileList(local_file_list_txt)
    f.get_remoteFileList()
    f.margeFile()
    print f.remote_files
    f.download_files()
    f.update_localFileList(local_file_list_txt)
    timenow = time.localtime()
    datenow = time.strftime('%Y-%m-%d %h:%M:%s', timenow)
    logstr = u"%s 成功执行了备份\n" % datenow
    debug_print(logstr)