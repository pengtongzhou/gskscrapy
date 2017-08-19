import fetchtool.Asyncfetch as myscrapy
from sys import argv
import pdb,time
#从dos环境中获取argv
file_main,theme=argv

#创建一个类并导入.josn、theme的相关性息
URLS=myscrapy.webclass()
URLS.setconfig(theme)
URLS.seturl(URLS.cnf['argurl'])
URLS.setxslt(URLS.cnf['theme'])

myscrapy.fetch_text(URLS.urls,URLS.xslt,URLS.cnf['code'],URLS.cnf['cookie'],theme)

# f=lambda a:map(lambda b:a[b:b+4],range(0,len(a),4))
# arv=f(URLS.urls)
# for i in arv:
#     myscrapy.fetch_text(i,URLS.xslt,URLS.cnf['code'],URLS.cnf['cookie'],theme)
#     time.sleep(15)