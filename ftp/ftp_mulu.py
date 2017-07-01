#配套ftp2一起研究一下 
import ftplib, os
conn = ftplib.FTP()
conn.connect('10.10.22.90')
conn.login()
dirname = "linux"
def downloaddir(dirname):
      os.mkdir(dirname)
      os.chdir(dirname)
      conn.cwd(dirname)
      print("change diretocry into "+dirname+' to download....')
      filelines = []
      conn.dir(filelines.append)
      filelines_bk = conn.nlst()
      i = 0
      for file in filelines:
           if 'd' in file.split()[0]:
               downloaddir(filelines_bk[i])
               conn.cwd('..')
               os.chdir('..')
               print("back to upper directory to downlaod....")
           else:
               fd = open(filelines_bk[i], 'wb')
               conn.retrbinary('RETR'+filelines_bk[i], fd.write)
           fd.close()
           i += 1
           print(filelines_bk[i] + 'download done....')
      conn.quit()
