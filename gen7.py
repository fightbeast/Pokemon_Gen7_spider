# -*- coding: utf-8 -*-
import  urllib2

import  urllib
import re
import BeautifulSoup

#处理页面标签类
class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x.strip()

class BDTB:

    def __init__(self,baseUrl,seeLZ):
        self.baseURL = baseUrl
        self.seeLZ = 'see_lz='+str(seeLZ)
        self.tool = Tool()
    def getPage(self,pageNum):
        try:
            url = self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            #print response.read()
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print  "fail to connect baidu tieba"
                return None

    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('.*?(.*?)',re.S)
        result = re.search(pattern,page)
        if result:
            # print result.group(1)
            return result.group(1).strip()
        else:
            return None


    def getTitle(self,page):

        pattern = re.compile('<h3 class="core_title_txt pull-left text-overflow  " title="(.*?)"', re.S)
        result = re.search(pattern,page)
        if result:
            #print result.group(1)
            return result.group(1).strip()
        else:
            return None

    # 获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?" class="d_post_content j_d_post_content ">(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = ( "\n"+self.tool.replace(item)+"  Page:"+str(x))
            contents.append(content.encode('utf-8'))
        return contents
        #print self.tool.replace(items[10])

baseURL = 'https://tieba.baidu.com/p/5096421119?'
bdtb = BDTB(baseURL,0)
pagenum = 54
content = []

for x in range(1,pagenum+1):
    page = bdtb.getPage(x)
    print bdtb.getTitle(page)+" Page "+str(x)
    content = bdtb.getContent(page)
    fo = open("gen7.txt", "a")#a接着写
    fo.writelines(content)
    fo.close()



input("\n\nPress the enter key to exit.")
