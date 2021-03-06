
# -*- encoding: utf8 -*-
import os
import sys
from ftplib import FTP
import socket

class FTPSync(object):
    def __init__(self, rootdir_local, hostaddr, username, password, remotedir, port=21):
        self.hostaddr = hostaddr
        self.username = username
        self.password = password
        self.remotedir = remotedir
        self.rootdir_local = rootdir_local
        self.port = port
        self.ftp = FTP()
    def login(self):
        ftp = self.ftp
        try:
            timeout = 300
            socket.setdefaulttimeout(timeout)
            ftp.set_pasv(True)
            print u'开始连接到 %s' % (self.hostaddr)
            ftp.connect(self.hostaddr, self.port)
            print u'成功连接到 %s' % (self.hostaddr)
            print u' %s开始登录' % (self.username)
            ftp.login(self.username, self.password)
            print u'成功登录到 %s' % (self.hostaddr)
            debug_print(ftp.getwelcome())
        except Exception:
            print u'连接或登录失败'
        try:
            #self.ftp.cwd('/')  # 远端FTP目录
            ftp.cwd(self.remotedir)
            if not os.path.isdir(self.rootdir_local):
                os.makedirs(self.rootdir_local)
            os.chdir(self.rootdir_local)  # 本地下载目录
        except(Exception):
            print u'切换目录失败'
    def get_dirs_files(self):
        u''' 得到当前目录和文件, 放入dir_res列表 '''
        dir_res = []
        self.ftp.dir('.', dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return (files, dirs)
    #def startbak(self):

    def walk(self, next_dir,local_dir='@$'):
        if local_dir=='@$':
            local_dir=next_dir
        print 'Walking to', next_dir.decode('utf-8')
        self.ftp.cwd(next_dir)
        try:
            os.mkdir(local_dir.decode('utf-8'))
        except OSError:
            pass
        t = local_dir.decode('utf-8')
        print t
        os.chdir(t)

        ftp_curr_dir = self.ftp.pwd()
        local_curr_dir = os.getcwd()

        files, dirs = self.get_dirs_files()
        print "FILES: ", files
        print "DIRS: ", dirs
        for f in files:
            print local_curr_dir,'保存',next_dir, ':', f
            outf = open(f.decode('utf-8'), 'wb')
            try:
                self.ftp.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
        for d in dirs:
            print local_curr_dir, '切换目录'
            os.chdir(local_curr_dir)
            self.ftp.cwd(ftp_curr_dir)
            self.walk(d)
    def run(self):
        self.walk(self.remotedir,self.rootdir_local)
        #self.walk('.')

def main(rootdir_local, hostaddr, username, password, remotedir, port):
    f = FTPSync(rootdir_local, hostaddr, username, password, remotedir, port)
    f.login()
    f.run()
def get_serverlist():
    print u'从 %s 中读取服务器列表' % (local_file_list_txt)
    try:
        fileTxt = open(local_file_list_txt, 'r')
    except Exception, e:
        print e
    for line in fileTxt:
        if '\xef\xbb\xbf' in line:
            line = line.replace('\xef\xbb\xbf', '')  # 用replace替换掉'\xef\xbb\xbf'
        line = line.strip('\n')
        line = line.strip(' ')
        local_files.append(line)

if __name__ == '__main__':
    rootdir_local = 'E:/temp/12'  # 本地目录
    rootdir_remote = '/'  # 远程目录
    local_file_list_txt = 'E:/temp/12/fileList.txt'    #配置文件
    local_files = []
    get_serverlist()
    print local_files
    for ser in local_files:
        ser=eval(ser)
        print "开始备份："+ser["name"]
        hostaddr = ser["hostaddr"]  # ftp地址
        username = ser["username"] # 用户名
        password = ser["password"]  # 密码
        port = ser["port"]  # 端口号
        rootdir_local = ser["localdir"]  # 本地目录
        rootdir_remote = ser["remotedir"]  # 远程目录
        main(rootdir_local, hostaddr, username, password, rootdir_remote, port)
#解决每个第二次备份的目录都在前一次的都后一个文件夹下面