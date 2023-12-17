import json  
import threading  
import time  
import DownloadMonitoringPages  
from Utils import Paths  
#import MonitorUrls  
import MonitorUrlsV2
  
def auto_save():  
    with open(Paths.settingJsonPath, 'r') as f:  
        settings = json.load(f)  
    saveCycleTime = settings['saveCycleTime']  
  
    while True:  
        DownloadMonitoringPages.DownloadMonitoringPages()  # 调用网页下载函数
        print("\n\n输入选项: 1:新增监控URL, 2:取消监控URL, 3:取消监控不可用的URL: \n")
        time.sleep(saveCycleTime)  # 等待指定的循环时间 

  
def receive_input():  
    while True:  
        choice = input("输入选项: 1:新增监控URL, 2:取消监控URL, 3:取消监控不可用的URL: \n")  
        if choice == '1':  
            targetUrl = input("请输入要新增的监控URL：\n")  
            #MonitorUrls.AddMonitoringUrl(new_url)  
            MonitorUrlsV2.AddUrl(targetUrl)
            DownloadMonitoringPages.DownloadMonitoringPages()
        elif choice == '2':  
            targetUrl = input("请输入要取消监控的URL：\n")  
            #MonitorUrls.DeleteMonitoringUrl(target_url) 
            MonitorUrlsV2.DeleteUrl(targetUrl) 
        elif choice == '3':  
            #MonitorUrls.DeleteInvalidUrls() 
            MonitorUrlsV2.DeleteInvalidUrls()  
        else:  
            print("无效的输入，请重新输入。\n")  
  
if __name__ == "__main__":  
    download_thread = threading.Thread(target=auto_save)  
    input_thread = threading.Thread(target=receive_input)  
  
    download_thread.start()  # 开始运行自动保存线程  
    input_thread.start()  # 开始运行用户输入线程