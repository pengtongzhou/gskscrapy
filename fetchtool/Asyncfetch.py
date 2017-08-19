from . import Asyncscrapy
import pandas as pd
from urllib import request
from urllib.parse import quote
import re,json,time,pdb
def fetch_text(urls,xslt,code,cookie,dis):
    dd = Asyncscrapy.Download()
    dd.data_concat(urls,xslt,code,cookie,dis)

class webclass(object):
    def __init__(self):
        self.pat=r'(.*?)\[(\[.*?\])\](.*)'

    def seturlFromMem(self,url):
        self.url=url
        pattern=re.compile(self.pat)
        gr=pattern.search(self.url)
        ar=json.loads(gr.group(2))
        self.urls=[gr.group(1) + str(i) + gr.group(3) for i in range(ar[0],ar[1],ar[2]) ]

    def seturlFromFile(self,fileName):
        self.fileName=fileName
        df=pd.read_excel(fileName,0)
        self.urls=df['URL']

    def seturl(self,argurl):
        switch={0:lambda x:self.seturlFromFile(x),1:lambda x:self.seturlFromMem(x)}
        switch['://' in argurl](argurl)

    def setxsltFromweb(self,apiurl):
        theme=apiurl.split('&theme=')
        theme[1]=quote(theme[1])
        apiurl = '&theme='.join(theme)
        self.xslt=request.urlopen(apiurl).read()

    def setxsltFromFile(self,apifile):
        with open(apifile,'r+',encoding="utf-8") as f:
            self.xslt=f.read()

    def setxslt(self,argxslt):
        switch={0:lambda x:self.setxsltFromFile(x),1:lambda x:self.setxsltFromweb(x)}
        switch['://' in argxslt](argxslt)

    def setconfig(self,config):
        with open( "./爬虫配置/" + config + "/" + config + ".json",'r',encoding='UTF-8') as f:
            self.cnf=json.loads(f.read())
        
