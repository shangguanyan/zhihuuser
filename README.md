# zhihuuser


## 安装

### 安装Python

至少Python3.5以上

### 安装scrapy

#### 安装依赖
	window安装
	1. wheel
	pip install wheel
	2.lxml
	 可以下载后whl文件，本地安装

	3.pyOpenSSL

	4.Twisted

	5.Pywin32
	 
```

#### 启动

```
scrapy crawl zhihu
```

## 说明：
	现知乎需要登陆后才能抓取相应的用户信息，
	所以需要在setting文件中配置相应的cookies

