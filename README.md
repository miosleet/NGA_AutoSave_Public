# NGA网页自动保存工具

## 00.私货

猛盒犹的瓜，香  
AI写代码真好用

## 1.目的

在NGA里吃瓜的时候，有时候瓜太离谱，导致瓜炸了，非常可惜  
这时候就需要有一个工具，来把瓜给保存下来，定时刷新保存，方便后续吃瓜，或者分享瓜  

## 2.文件结构

**NGA_AutoSave.py：启动文件**  
CookieFormat.py：处理Cookie。向NGA发送请求的时候，需要带上Cookie  
DownloadMonitoringPages.py：主要的下载网页的代码  
MonitorUrls.py：记录监控中的url  
Paths.py：记录了一些路径  
./Settings/cookie.txt：用户粘贴自己的Cookie（"./"代表相对于NGA_AutoSave.py的位置，"."相当于NGA_AutoSave.py这个文件所在的文件夹）  
./Settings/setting.json：配置文件  

## 3.使用方法

### 3.0.安装Python

这个再怎么说也不应该不知道吧  
不知道怎么用就搜一下好了  
Python3.7就可以用了，更高版本的可以向下兼容  

### 3.1.获取Cookie：
以使用Chrome为例：  
打开NGA的网页，按F12进入开发者工具，在Application->Cookies里，复制自己的Cookie  
![image](https://github.com/miosleet/NGA_AutoSave/assets/43563705/0df3509e-e4b9-4edd-ac38-84eb91e02963)  
粘贴到./Settings/cookie.txt文件内  

### 3.2.设置保存网页的路径（可选）

打开./Settings/setting.json，找到"saveHtmlFolderPath"，这里记录了保存网页文件的位置。  
默认情况下，会保存在"./PageSaved/"文件夹，即NGA_AutoSave.py所在文件夹内的PageSaved文件夹。  
你也可以以绝对路径的形式记录保存路径  

### 3.3.开始自动保存网页

运行NGA_AutoSave.py  
初次运行时，会提示URL列表为空，这没有问题。  
复制一个需要监控（自动保存）的NGA帖子的1楼的URL（如）https://bbs.nga.cn/read.php?tid=38694078  
根据提示，新增监控URL，输入1，回车，即可选择新增监控的URL  
粘贴刚刚复制的URL，回车，即可开始监视这个URL  
![image](https://github.com/miosleet/NGA_AutoSave/assets/43563705/0bba8e6c-1782-4938-8069-052e2aeca85b)  
在开始监视时，会自动将这个帖子里的每一页保存下来  
后续，每3分钟会进行一次下载  

### 3.4.找到下载的网页

下载的网页保存会在3.2里设置的位置，每个帖子归档在一个以帖子标题为文件夹名称的文件夹里  

### 3.5.修改监控中的网页

NGA_AutoSave.py运行时，有3个选择：1:新增监控URL, 2:取消监控URL, 3:取消监控不可用的URL  
新增监控和取消监控URL，都需要输入目标URL。  
**当网页被隐藏、冲水等原因导致无法访问时，帖子会变得不可用（当然，已经保存的本地文件可以正常打开）**  
当你不知道你监控了哪些网页时，关闭再打开NGA_AutoSave.py，最上面就会显示正在监控哪些URL  
（当然，也可以直接去./Settings/setting.json查找并修改，但是我不建议没看源码的人乱改。因为我也不保证这么改不会出错，鲁棒性超差的。能跑就不要改.jpg）  

## 4.特性

1.监控中的网页会记录末页页码，也就是当第一次保存全部页面之后，后续的每次下载均只会下载上一次末页及其之后的页面（也就是说，之前的页面不会修改，即便之前的页面里有人删了自己的发言）  
2.每3分钟180秒一次自动保存。如果你觉得太慢了，也可以修改./Settings/setting.json中的saveCycleTime来修改，单位是秒。 
3.非标准命名方式（习惯大驼峰命名函数了，改不了）

## 5.TODO（但是Lazy）

**1.可视化**  
2.貌似当帖子标题改了之后，会重新保存到另一个文件夹，这个没法处理  
3.输入Cookie很麻烦，有没有办法能够直接复制Cookie。当然直接读取Cookie文件貌似不行，加密了  
4.每次添加监控目标URL都要手动复制很麻烦，看看能不能简化操作  
5.添加监控URL必须是第一页的URL，即没有&page=...，看看要不要改（能跑就不要改.jpg）    
6.编译为exe，虽然我觉得没有太大必要就是了  
**7.版面热贴自动加入监视**，可以监视几个特定版面，然后也定时抓一下回帖数量，超过阈值的帖子URL加入监视  
8.帖子TTL，超过一定时间没有新回复（或者页面数量增长），则记为坟贴，不再监视  
9.峰谷刷新率，每次刷新间隔跟随时间变化而波动，以减少闲时的访问NGA的次数
