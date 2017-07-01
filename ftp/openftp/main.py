import ftp
f=ftp.ftp()
f.open('ftp.sjtu.edu.cn',21)
 
f.username('ftp')
 
f.password('ftp')

f.dir(None)
