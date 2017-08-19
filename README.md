# 前言

## 本爬虫的框架是基于tornado,核心的提取器来自Gooseeker的xslt

**给你200W条url，需要你把每个url对应的页面抓取保存起来，这种时候，单单使用多进程，效果肯定是很差的。为什么呢？**

1. 例如每次请求的等待时间是2秒，那么如下（忽略cpu计算时间）：

1. 单进程+单线程：需要2秒*200W=400W秒==1111.11个小时==46.3天，这个速度明显是不能接受的
 
1. 单进程+多线程：例如我们在这个进程中开了10个多线程，比1中能够提升10倍速度，也就是大约4.63天能够完成200W条抓取，请注意，这里的实际执行是：线程1遇见了阻塞，CPU切换到线程2去执行，遇见阻塞又切换到线程3等等，10个线程都阻塞后，这个进程就阻塞了，而直到某个线程阻塞完成后，这个进程才能继续执行，所以速度上提升大约能到10倍（**这里忽略了线程切换带来的开销，实际上的提升应该是不能达到10倍的**），但是需要考虑的是线程的切换也是有开销的，所以不能无限的启动多线程（开200W个线程肯定是不靠谱的）

1. 多进程+多线程：这里就厉害了，一般来说也有很多人用这个方法，多进程下，每个进程都能占一个cpu，而多线程从一定程度上绕过了阻塞的等待，所以比单进程下的多线程又更好使了，例如我们开10个进程，每个进程里开20W个线程，执行的速度理论上是比单进程开200W个线程快10倍以上的（为什么是10倍以上而不是10倍，主要是cpu切换200W个线程的消耗肯定比切换20W个进程大得多，考虑到这部分开销，所以是10倍以上）
 


 还有更好的方法吗？答案是肯定的，它就是：协程。如果当前请求正在等待来自其他资源的数据（比如数据库查询或HTTP请求）时，一个**协程**可以明确地控制以挂起请求。本程序是基于tornado的协程处理的爬虫，有极高的并发处理能力，**（注意:高并发也意味着可能会被ban,使用时候记得注意控制下并发数，）**

在run.py使用如下这段代码可以控制并发数在400左右，根据实际的情况而定。

<pre>    
    f=lambda a:map(lambda b:a[b:b+400],range(0,len(a),400))

    arv=f(URLS.urls)

    for i in arv:

        myscrapy.fetch_text(i,URLS.xslt,URLS.cnf['code'],URLS.cnf['cookie'],theme)

        time.sleep(15)
</pre>

# 一、安装（图文具体见readme.html）

1、安装python3.6

2、在gsk.cmd的目录下打开命令行运行：

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirement.txt
```

# **二、创建项目的操作**

按下shif键的同时右键，选择“在此处打开命令窗口”

使用命令 gsk创建一个爬虫项目，例如：

```
gsk  job51
```

进行上一步操作之后会在目录“爬虫配置”下，生成job51.xlsx、job51.json、job51.txt、job51.xml它们分别代表着要抓取的网址，爬虫的核心配置，cookie值,xslt规则文件。

# 三、*.json的参数说明

接了来是重点，修改job51.json。job51.json有四个参数：“argurl、theme、code、cookie”‘。下文来一一讲述。

<pre>
{
    "argurl": "http://search.51job.com/list/030000,000000,0000,00,9,99,%E8%B4%B7%E6%AC%BE,2,[[1,12,1]].html",

    "theme": "./爬虫配置/job51/job51.xml",

    "code":"gbk",

    "cookie":"./爬虫配置/job51/job51.txt"
    }
</pre>

## argurl的参数（两种的形式）

> **第一种形式：**,“./爬虫配置/job51/job51.xlsx”。也就是job51.json所在目录下的job51.xlsx文件，需要把如下的链接放入job51.xlsx的sheet1表中即可,注意复制到A1单元格。  

| URL|
|----|
| https://www.baidu.com/s?wd=BDV-704321558 |
| https://www.baidu.com/s?wd=BDV-245662521 |
| https://www.baidu.com/s?wd=BDV-704914839 |
| https://www.baidu.com/s?wd=BDV-313409633 |
| https://www.baidu.com/s?wd=BDV-428998430 |
| https://www.baidu.com/s?wd=BDV-359794212 |
| https://www.baidu.com/s?wd=BDV-616619857 |
| https://www.baidu.com/s?wd=BDV-237426602 |
| https://www.baidu.com/s?wd=BDV-344147147 |
| https://www.baidu.com/s?wd=BDV-389896018 |
| https://www.baidu.com/s?wd=BDV-470443161 |
| https://www.baidu.com/s?wd=BDV-110492874 |
| https://www.baidu.com/s?wd=BDV-294834881 |


> **第二种形式：**“http://search.51job.com/\*\*,[[1,12,1]].html”。在这里"[[1,12,1]]”代表的是从http://search.51job.com/\*\*,1.html到http://search.51job.com/**,12.html的步长为一的网址序列

## **theme参数（两种的形式）：**

> **第一种形式：**"./爬虫配置/job51/job51.xml"，也就是job51.json所在目录下的job51.xml文件，这个文件的内容遵循xlst规则。可以由gooseeker谋数台获得。**<span style="color:#FF0000">（注意：“<?xml version="1.0" encoding="UTF-8"?>”去掉）</span>**

<pre>
&lt;xsl:stylesheet version=&quot;1.0&quot; xmlns:xsl=&quot;http://www.w3.org/1999/XSL/Transform&quot; &gt;
&lt;xsl:template match=&quot;/&quot;&gt;
&lt;company&gt;
&lt;xsl:apply-templates select=&quot;//*[@id=&#39;resultList&#39;]/div[position()&gt;=3 and count(./following-sibling::div[position()=1]/span[position()=1]/a/text())&gt;0]&quot; mode=&quot;company&quot;/&gt;
&lt;/company&gt;
&lt;/xsl:template&gt;
&lt;xsl:template match=&quot;//*[@id=&#39;resultList&#39;]/div[position()&gt;=3 and count(./following-sibling::div[position()=1]/span[position()=1]/a/text())&gt;0]&quot; mode=&quot;company&quot;&gt;
&lt;item&gt;
&lt;名称&gt;
&lt;xsl:value-of select=&quot;following-sibling::div[position()=1]/span[position()=1]/a/text()&quot;/&gt;
&lt;/名称&gt;
&lt;URL&gt;
&lt;xsl:value-of select=&quot;following-sibling::div[position()=1]/span[position()=1]/a/@href&quot;/&gt;
&lt;/URL&gt;
&lt;/item&gt;
&lt;/xsl:template&gt;
&lt;/xsl:stylesheet&gt;

</pre>



> **第二种形式：**“http://www.gooseeker.com/api/getextractor?key=[你的APPKEY]&theme=[你的主题]”。也就是你在gooseker上网页版本的xslt规则。

## code参数（一种形式，字符串）



> 一般是“utf-8”,如果遇到有乱码的网页，改成“gbk”

## cookie参数（一种形式，文件）



> 获取的是job51.txt的内容，当某些网站需要登录才能采集的时候。可以把登录状态下的cookie复制到job51.txt。一般在任意一款浏览器的控制台下输入document.cookie即可查看。

# 运行爬虫

gsk.cmd的目录下运行:

```
gsk job51
```

之后会当前的data目录下创建job51目录，数据都存放在这里,其他的项目类似，只有gooseeker通过成功的规则都可以用。