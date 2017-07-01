# Author by Andy
# _*_ coding:utf-8 _*_
'''
This program is used to create a ftp client

'''
import socket, os, json, time, hashlib, sys


class Ftp_client(object):
    def init(self):
        self.client = socket.socket()

    def help(self):
        msg = '''useage:
  ls
  pwd
  cd dir(example: / .. . /var)
  put filename
  rm filename
  get filename
  mkdir directory name
  '''
        print(msg)

    def connect(self, addr, port):
        self.client.connect((addr, port))

    def auth(self):
        m = hashlib.md5()
        username = input("请输入用户名：").strip()

        m.update(input("请输入密码：").strip().encode())
        password = m.hexdigest()
        user_info = {
            'action': 'auth',
            'username': username,
            'password': password}
        self.client.send(json.dumps(user_info).encode('utf-8'))
        server_response = self.client.recv(1024).decode()
        # print(server_response)
        return server_response

    def interactive(self):
        while True:
            msg = input(">>>:").strip()
            if not msg:
                print("不能发送空内容！")
                continue
            cmd = msg.split()[0]
            if hasattr(self, cmd):
                func = getattr(self, cmd)
                func(msg)
            else:
                self.help()
                continue

    def put(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            if os.path.isfile(filename):
                filesize = os.stat(filename).st_size
                file_info = {
                    "action": "put",
                    "filename": filename,
                    "size": filesize,
                    "overriding": 'True'
                }
                self.client.send(json.dumps(file_info).encode('utf-8'))
                # 防止粘包，等待服务器确认。
                request_code = {
                    '200': 'Ready to recceive data!',
                    '210': 'Not ready to received data!'
                }
                server_response = self.client.recv(1024).decode()
                if server_response == '200':
                    f = open(filename, "rb")
                    send_size = 0
                    start_time = time.time()
                    for line in f:
                        self.client.send(line)
                        send_size += len(line)
                        send_percentage = int((send_size / filesize) * 100)
                        while True:
                            progress = ('\r已上传%sMB(%s%%)' % (round(send_size / 102400, 2), send_percentage)).encode(
                                'utf-8')
                            os.write(1, progress)
                            sys.stdout.flush()
                            time.sleep(0.0001)
                            break
                    else:
                        end_time = time.time()
                        time_use = int(end_time - start_time)
                        print("\nFile %s has been sent successfully!" % filename)
                        print('\n平均下载速度%s MB/s' % (round(round(send_size / 102400, 2) / time_use, 2)))
                        f.close()
                else:
                    print("Sever isn't ready to receive data!")
                    time.sleep(10)
                    start_time = time.time()
                    f = open(filename, "rb")
                    send_size = 0
                    for line in f:
                        self.client.send(line)
                        send_size += len(line)
                        # print(send_size)
                        while True:
                            send_percentage = int((send_size / filesize) * 100)
                            progress = ('\r已上传%sMB(%s%%)' % (round(send_size / 102400, 2), send_percentage)).encode(
                                'utf-8')
                            os.write(1, progress)
                            sys.stdout.flush()
                            # time.sleep(0.0001)
                            break
                    else:
                        end_time = time.time()
                        time_use = int(end_time - start_time)
                        print("File %s has been sent successfully!" % filename)
                        print('\n平均下载速度%s MB/s' % (round(round(send_size / 102400, 2) / time_use, 2)))
                        f.close()
            else:
                print("File %s is not exit!" % filename)
        else:
            self.help()

    def ls(self, *args):
        cmd_split = args[0].split()
        # print(cmd_split)
        if len(cmd_split) > 1:
            path = cmd_split[1]
        elif len(cmd_split) == 1:
            path = '.'
        request_info = {
            'action': 'ls',
            'path': path
        }
        self.client.send(json.dumps(request_info).encode('utf-8'))
        sever_response = self.client.recv(1024).decode()
        print(sever_response)

    def pwd(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) == 1:
            request_info = {
                'action': 'pwd',
            }
            self.client.send(json.dumps(request_info).encode("utf-8"))
            server_response = self.client.recv(1024).decode()
            print(server_response)
        else:
            self.help()

    def get(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            file_info = {
                "action": "get",
                "filename": filename,
                "overriding": 'True'
            }
            self.client.send(json.dumps(file_info).encode('utf-8'))
            server_response = self.client.recv(1024).decode()  # 服务器反馈文件是否存在
            self.client.send('0'.encode('utf-8'))
            if server_response == '0':
                file_size = int(self.client.recv(1024).decode())
                # print(file_size)
                self.client.send('0'.encode('utf-8'))  # 确认开始传输数据
                if os.path.isfile(filename):
                    filename = filename + '.new'
                f = open(filename, 'wb')
                receive_size = 0
                m = hashlib.md5()
                start_time = time.time()
                while receive_size < file_size:
                    if file_size - receive_size > 1024:  # 还需接收不止1次
                        size = 1024
                    else:
                        size = file_size - receive_size
                    data = self.client.recv(size)
                    m.update(data)
                    receive_size += len(data)
                    data_percent = int((receive_size / file_size) * 100)
                    f.write(data)
                    progress = ('\r已下载%sMB(%s%%)' % (round(receive_size / 102400, 2), data_percent)).encode('utf-8')
                    os.write(1, progress)
                    sys.stdout.flush()
                    time.sleep(0.0001)

                else:
                    end_time = time.time()
                    time_use = int(end_time - start_time)
                    print('\n平均下载速度%s MB/s' % (round(round(receive_size / 102400, 2) / time_use, 2)))
                    Md5_server = self.client.recv(1024).decode()
                    Md5_client = m.hexdigest()
                    print('文件校验中，请稍候...')
                    time.sleep(0.3)
                    if Md5_server == Md5_client:
                        print('文件正常。')
                    else:
                        print('文件与服务器MD5值不符，请确认！')
            else:
                print('File not found!')
                client.interactive()
        else:
            self.help()

    def rm(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            filename = cmd_split[1]
            request_info = {
                'action': 'rm',
                'filename': filename,
                'prompt': 'Y'
            }
            self.client.send(json.dumps(request_info).encode("utf-8"))
            server_response = self.client.recv(10240).decode()
            request_code = {
                '0': 'confirm to deleted',
                '1': 'cancel to deleted'
            }

            if server_response == '0':
                confirm = input("请确认是否真的删除该文件：")
                if confirm == 'Y' or confirm == 'y':
                    self.client.send('0'.encode("utf-8"))
                    print(self.client.recv(1024).decode())
                else:
                    self.client.send('1'.encode("utf-8"))
                    print(self.client.recv(1024).decode())
            else:
                print('File not found!')
                client.interactive()


        else:
            self.help()

    def cd(self, *args):
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            path = cmd_split[1]
        elif len(cmd_split) == 1:
            path = '.'
        request_info = {
            'action': 'cd',
            'path': path
        }
        self.client.send(json.dumps(request_info).encode("utf-8"))
        server_response = self.client.recv(10240).decode()
        print(server_response)

    def mkdir(self, *args):
        request_code = {
            '0': 'Directory has been made!',
            '1': 'Directory is aleady exist!'
        }
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            dir_name = cmd_split[1]
            request_info = {
                'action': 'mkdir',
                'dir_name': dir_name
            }
            self.client.send(json.dumps(request_info).encode("utf-8"))
            server_response = self.client.recv(1024).decode()
            if server_response == '0':
                print('Directory has been made!')
            else:
                print('Directory is aleady exist!')
        else:
            self.help()
            # def touch(self,*args):


def run():
    client = Ftp_client()
    # client.connect('10.1.2.3',6969)
    Addr = input("请输入服务器IP：").strip()
    Port = int(input("请输入端口号：").strip())
    client.connect(Addr, Port)
    while True:
        if client.auth() == '0':
            print("Welcome.....")
            client.interactive()
            break
        else:
            print("用户名或密码错误！")
            continue
run()