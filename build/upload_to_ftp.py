#coding=utf-8
__author__ = 'dingkang'  
__mail__ = 'dingkang@ancun.com'  
__date__ = '2016-07-27'  
__version = 1.0  
  
import sys  
import os  
import json  
from ftplib import FTP
from urllib import unquote
  
_XFER_FILE = 'FILE'  
_XFER_DIR = 'DIR'  
  
class Xfer(object):  
    ''''' 
    @note: upload local file or dirs recursively to ftp server 
    '''  
    def __init__(self):  
        self.ftp = None  
      
    def __del__(self):  
        pass  
      
    def setFtpParams(self, ip, uname, pwd, port = 21, timeout = 60):          
        self.ip = ip  
        self.uname = uname  
        self.pwd = pwd  
        self.port = port  
        self.timeout = timeout  
      
    def initEnv(self):  
        if self.ftp is None:  
            self.ftp = FTP()  
            print '### connect ftp server: %s ...'%self.ip  
            self.ftp.connect(self.ip, self.port, self.timeout)  
            self.ftp.login(self.uname, self.pwd)   
            print self.ftp.getwelcome()  
      
    def clearEnv(self):  
        if self.ftp:  
            self.ftp.close()  
            print '### disconnect ftp server: %s!'%self.ip   
            self.ftp = None  
      
    def uploadDir(self, localdir='./', remotedir='./'):  
        if not os.path.isdir(localdir):    
            return  
        self.ftp.cwd(remotedir)   
        for file in os.listdir(localdir):  
            src = os.path.join(localdir, file)  
            if os.path.isfile(src):  
                self.uploadFile(src, file)  
            elif os.path.isdir(src):  
                try:    
                    self.ftp.mkd(file)    
                except:    
                    sys.stderr.write('the dir is exists %s'%file)  
                self.uploadDir(src, file)  
        self.ftp.cwd('..')  
      
    def uploadFile(self, localpath, remotepath='./'):  
        if not os.path.isfile(localpath):    
            return  
        print '+++ upload %s to %s:%s'%(localpath, self.ip, remotepath)
        try: 
            f = open(localpath, 'rb')
            cmd = 'STOR ' + remotepath
            self.ftp.storbinary(cmd, f)
        except Exception, e:
            print '+++ upload failed %s to %s:%s'%(localpath, self.ip, remotepath)

    def mkdir(self, remotepath='./'):
        self.initEnv()
        if remotepath == './':
            return
        try:
            self.ftp.cwd(remotepath)
            prinf('path exist')
            ##self.ftp.cwd('/')
            return
        except Exception, e:
            print('path not exist, mkdir')
            try:
                self.ftp.mkd(remotepath)
                return
            except Exception, e:
                print('create path failed')
                return
        return
      
    def __filetype(self, src):  
        if os.path.isfile(src):  
            index = src.rfind('\\')  
            if index == -1:  
                index = src.rfind('/')                  
            return _XFER_FILE, src[index+1:]  
        elif os.path.isdir(src):  
            return _XFER_DIR, ''          
      
    def upload(self, src, remotepath):  
        filetype, filename = self.__filetype(src)  
          
        self.initEnv()  
        if filetype == _XFER_DIR:  
            self.srcDir = src
            self.uploadDir(self.srcDir, remotepath)
        elif filetype == _XFER_FILE:  
            self.uploadFile(filename, remotepath)
        self.clearEnv()

def getversion(filename):
    try: 
        import xml.etree.cElementTree as ET
    except ImportError: 
        import xml.etree.ElementTree as ET
    import sys
        
    try:
        tree = ET.parse(filename)    
        root = tree.getroot() 
        entry = root.find('entry')
        commit = entry.find('commit')
        revision = commit.get('revision')
        return revision
    except Exception, e:
        print "Error:cannot parse file:Version.xml."
        return ''
		
def getrelativalpath(filename):
    try: 
        import xml.etree.cElementTree as ET
    except ImportError: 
        import xml.etree.ElementTree as ET
    import sys
        
    try:
        tree = ET.parse(filename) 
        root = tree.getroot() 
        entry = root.find('entry')
        relativeurl = entry.find('relative-url').text
        if relativeurl==None:
            print "relativeurl is None"
            return ''
        svnrelativalpath = relativeurl[1:]
        svnrelativalpath = svnrelativalpath + '/'
        print svnrelativalpath
        return svnrelativalpath
    except Exception, e:
        print "Error:cannot parse file:Version.xml."
        return ''

if __name__ == '__main__':
    srcFile = sys.argv[1]
    version = getversion('Version.xml')
    relativalpath = getrelativalpath('Version.xml')
    #svn方式和git方式生成的Version.xml文件不一样
    #svn方式是目录结构，可以直接使用项目的相对路径作为ftp的相对目录，
    #git方式没有项目相对目录，使用脚本中写死的路径作为相对目录
    if version=='':
        sys.exit(1)
    if relativalpath=='':
        relativalpath=sys.argv[2]
    remotefullpath = relativalpath + version + '/' + srcFile
    relativalpath = relativalpath + version + '/'
    remotefullpath = unquote(remotefullpath).decode('utf8').encode('gbk')
    relativalpath = unquote(relativalpath).decode('utf8').encode('gbk')
    srcFile = unquote(srcFile).decode('utf8').encode('gbk')
    xfer = Xfer()
    xfer.setFtpParams(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    xfer.mkdir(relativalpath)
    xfer.upload(srcFile, remotefullpath)
    sys.exit(0)
