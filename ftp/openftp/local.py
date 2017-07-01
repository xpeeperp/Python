import ftp
f=ftp.ftp()

f.open('localhost',21)
f.getcurrentdir()
f.username('bear')

f.password('bear')
f.setDataMode("BINARY")
f.setDataCompressMode("ZLIB")
f.downloadfile('test.png','test.png')
f.getfilesize('Jemy')
f.getserversystemtype()
f.getremotehelp(None)
f.disconnect()