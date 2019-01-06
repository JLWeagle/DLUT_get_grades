# DUTer成绩查询  
*从教务处网站查询成绩，使用 `requests` 和 `BeautifulSoup4`模块。*  
目前有如下功能：  
- 查询本学期成绩  
- 查询全部成绩  
- 将中文成绩单保存至本地  
- 定时查看成绩更新并发送邮件通知  

请确保您已安装如下模块：  
```
 pip install requests   
 pip install BeautifulSoup4   
```

## 使用方法  
1. 修改`confs.json`内的登录、收发邮件邮箱信息。  
2. 到程序目录下运行`get_grades.py`  
```
 python3 get_grades.py
```
