'''
TODO
response.text可以读到
<a href='/read.php?tid=38670883&page=1' title='上一页'class='pager_spacer'>上一页(1)</a>
<a href='/read.php?tid=38670883&page=3' title='下一页'class='pager_spacer'>下一页(3)</a>
这在直接打开网页时是没有的，注意。
通过存在“page=3' title='下一页'class='pager_spacer'>下一页”来判断是否有下一页，如果有，则继续访问下一页
需要给定一个起始页，会从起始页开始保存
'''

import os  
import requests  
import CookieFormat  
import Paths  
import MonitorUrls  
import re  
  
# 将 cookies 定义为全局变量  
cookies = None  
nextPage=1
  
def DownloadWebpage(url, filename, urlBase):  
    global cookies  # 声明使用全局变量 cookies  
    if not cookies:  # 如果 cookies 为空，则调用 CookieFormat.GetCookies() 获取 cookies  
        cookies = CookieFormat.GetCookies()  
    response = requests.get(url, cookies=cookies)  
    if response.status_code == 200:  
        match = re.search(r"\(ERROR:<!--msgcodestart-->\d+<!--msgcodeend-->\)", response.text)
        if(match):
            print(f"帖子{url}访问失败: {match.group()}")
            MonitorUrls.InvalidMonitoringUrls(urlBase)
            return None
        else:
            with open(filename, 'w', encoding='gbk') as file:  
                file.write(response.text)  
                print(f"网页已成功保存为 {filename}")  
                return response  # 返回成功请求时返回的response对象  
    else:  
        print(f"请求失败，状态码：{response.status_code}")  
        MonitorUrls.InvalidMonitoringUrls(urlBase)
        return None  # 返回请求失败时返回的None  
  

  
def DownloadWebpageSequence(urlBase, fileNameBase, page=1):  
    global nextPage
    if(page==1):
        url=urlBase
        fileName=fileNameBase + ".html"
    else:
        url = urlBase + "&page=" + str(page)  
        fileName=fileNameBase + "&page=" + str(page) + ".html"
    print(f"准备下载网页{url}") 
    response = DownloadWebpage(url, fileName, urlBase)  
    if response is not None:  
        match = re.search(r"title='下一页' class='pager_spacer'>下一页\(\d+\)</a>", response.text) 
        if match:  
            nextPage = int(match.group()[37:-5])  
            if nextPage > page:  
                print(f"存在下一页: {nextPage}") 
                DownloadWebpageSequence(urlBase, fileNameBase, nextPage)
        else:
            #当已经到了最后一页
            finalPage=page
            print(f"已经达到最后一页: {finalPage}")
            MonitorUrls.SetFinalPage(urlBase,finalPage)#记录最后一页的页码
            nextPage=1
            return finalPage
            
  
def DownloadMonitoringPages():  # 注意在def后添加了空格  
    monitoringUrls = MonitorUrls.GetMonitoringUrls()  
    if monitoringUrls:  
        for urlDict in monitoringUrls:  
            valid = urlDict.get("valid")  
            savedUrl = urlDict.get("savedUrl")  
            if valid:  
                if savedUrl:  
                    # 分割 savedUrl，获取 "tid=" 后的部分  
                    tidPart = savedUrl.split("tid=")[-1]  

                    # 修改文件夹名

                    global cookies  # 声明使用全局变量 cookies  
                    if not cookies:  # 如果 cookies 为空，则调用 CookieFormat.GetCookies() 获取 cookies  
                        cookies = CookieFormat.GetCookies()  
                    response = requests.get(savedUrl, cookies=cookies) 
                    pageTitle=""
                    if response.status_code == 200:  
                        match = re.search(r"<meta name='keywords' content=''><title>.*?</title>", response.text)
                        if(match):
                            pageTitle=match.group()[40:-8]

                    folderName = Paths.saveHtmlFolderPath + "tid_" + tidPart + "_" + pageTitle  
                    # 检查文件夹是否存在，如果不存在则创建文件夹，然后进行网页下载  
                    if not os.path.exists(folderName):  
                        try:  
                            os.makedirs(folderName)  
                        except OSError as e:  
                            print(f"创建文件夹时出错：{e}")  
                            continue  
                    fileNameBase = folderName + "/tid_" + tidPart  # 修正了fileNameBase的赋值，去掉了引入page的部分  
                    finalPage=MonitorUrls.GetFinalPage(savedUrl)
                    print(f"准备下载网页序列{savedUrl}，从{finalPage}页开始")  
                    DownloadWebpageSequence(savedUrl, fileNameBase,finalPage)  # 直接调用DownloadWebpageSequence函数，不再检查保存是否成功  
                else:  
                    print(f"获取到的 URL 列表中的{savedUrl}不是有效的 URL。")  
            else:  
                print(f"{savedUrl} 不可用。")  # 当 valid 为 false 时给出提示，内容为某某 URL 不可用  
        print("所有有效的 URL 已处理完毕。")  
    else:  
        print("获取到的 URL 列表为空。")
# 程序开始运行时调用DownloadMonitoringPages 函数，并初始化page变量（这里仅为示例，您需要根据实际情况进行赋值）   
DownloadMonitoringPages()

#print("aaaaaa")