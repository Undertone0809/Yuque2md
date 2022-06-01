## 1.简介

语雀直接导出的md里面如果有图片，会无法正常显示，该项目基于pyqt的框架做了一个快速转换器，将语雀导出的md文件进行转换，让markdown文件中的图片可以正常显示，方便使用。



直接拿exe文件:[【工具】修复语雀转md时图片无法正常外链显示的小工具](https://blog.csdn.net/linZinan_/article/details/125091337?csdn_share_tail=%7B%22type%22%3A%22blog%22%2C%22rType%22%3A%22article%22%2C%22rId%22%3A%22125091337%22%2C%22source%22%3A%22linZinan_%22%7D&ctrtid=dLJzN)



## 2.运行环境

- python3.7.6
- 使用pip安装下面的环境

```
pip install PyQt5
pip install request
pip install pymysql
pip install mysql
pip install dbutils
```

- 项目主入口: main.py



## 3.更多

- 本项目在pyqt的框架上进一步封装，基于springMVC架构和springboot架构进行二次架构设计，参考笔者之前写的：[【快速调用】基于mvc架构的pyqt架构封装](https://blog.csdn.net/linZinan_/article/details/112460133) 

- [基于pyqt和springMVC架构优化的疫情信息管理系统](https://github.com/Undertone0809/COVID-19-Info-management-system-based-on-pyqt)

